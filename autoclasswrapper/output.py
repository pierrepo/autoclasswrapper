import datetime
import zipfile

import numpy as np
import pandas as pd

import logging
log = logging.getLogger(__name__)

class Output():
    """
    Class to handle autoclass output files and results
    """

    def __init__(self, inputfolder='',
                       tolerate_error=False):
        """
        Object instanciation
        """
        self.inputfolder = inputfolder

        self.tolerate_error = tolerate_error
        self.had_error = False

        self.cases = []
        self.classes = []


    def handle_error(f):
        """
        Handle error during data parsing and formating
        """
        def try_function(self, *args, **kwargs):
            if self.tolerate_error or not self.had_error:
                try:
                    return f(self, *args, **kwargs)
                except Exception as e:
                    for line in str(e).split('\n'):
                        log.error(line)
                    self.had_error = True
        return try_function


    @handle_error
    def extract_results(self, case_name='clust.case-data-1'):
        """
        Extract results from autoclass

        """
        log.info("Extracting autoclass results")
        # first pass: get number of cases and classes
        self.class_number = 0
        self.case_number = 0
        classes = set()
        with open(case_name, 'r') as case_file:
            for line in case_file:
                if not line:
                    continue
                if line.startswith('#') or line.startswith('DATA'):
                    continue
                items = line.split()
                classes.add(int(items[1]))
                self.case_number += 1
            self.class_number = len(classes)
        log.info("Found {} cases classified in {} classes."
                     .format(self.case_number, self.class_number))
        # create dataframe
        columns = ["main-class", "main-prob"]
        for i in range(self.class_number):
            label = "prob-class-{}".format(i)
            columns.append(label)
        self.stats = pd.DataFrame(np.nan,
                                  index=np.arange(1, self.case_number+1),
                                  columns=columns)
        # second pass: fill dataframe
        with open(case_name, 'r') as case_file:
            for line in case_file:
                if not line:
                    continue
                if line.startswith('#') or line.startswith('DATA'):
                    continue
                items = line.split()
                assert len(items) >=0, \
                       ("Need case#, class and prob in {}:\n "
                        "{}\n"
                        .format(input_file, line.rstrip()))
                case = int(items[0])
                for idx in range(1, len(items), 2):
                    class_id = int(items[idx])
                    proba = float(items[idx+1])
                    if idx == 1:
                        self.stats.loc[case, "main-class"] = class_id
                        self.stats.loc[case, "main-prob"] = proba
                    label = "prob-class-{}".format(class_id)
                    self.stats.loc[case, label] = proba


    @handle_error
    def aggregate_input_data(self, datafile="clust.tsv"):
        """
        Aggregate autoclass classes with input data
        """
        log.info("Aggregating input data")
        self.df = pd.read_table(datafile, sep='\t', header=0, index_col=0)
        nrows, ncols = self.df.shape
        self.experiment_names = list(self.df.columns)
        assert len(self.stats.index) == nrows, \
               ("Number of cases found in results ({}) "
                "should match number of rows in input file ({})!"
                .format(len(self.stats.index), datafile))
        self.stats.index = self.df.index
        self.df = pd.concat([self.df, self.stats], axis=1)


    @handle_error
    def write_cdt(self, with_proba=False):
        """
        Writing .cdt file for visualisation
        """
        if not with_proba:
            log.info("Writing .cdt file")
        else:
            log.info("Writing .cdt file (with probs)")
        filename = "clust.cdt"
        if with_proba:
            filename = "clust_withprobs.cdt"
        # add GWEIGHT
        self.df["gweight"] = 1
        # add gene name twice for formatting purpose
        self.df["name1"] = self.df.index
        self.df["name2"] = self.df.index
        # build gid
        self.df["idx"] = np.arange(1, self.df.shape[0]+1, dtype=int)
        self.df["gid"] = self.df.apply(lambda x: "GENE{:04d}-CL{:03.0f}X"
                                                 .format(x["idx"],
                                                         x["main-class"]+1),
                                       axis=1)
        # sort by increasing class
        self.df.sort_values(by=['main-class', 'main-prob'],
                            ascending=[True, False],
                            inplace=True)
        with open(filename, 'w') as cdtfile:
            # write header line
            headers = ["GID", "UNIQID", "NAME", "GWEIGHT"]
            headers += self.experiment_names
            if with_proba:
                headers += ["prob-class-{}"
                            .format(i+1) for i in range(self.class_number)]
            cdtfile.write("{}\n".format("\t".join(headers)))
            # write 'EWEIGHT' line
            eweight = "EWEIGHT\t\t\t"+"\t1"*len(self.experiment_names)
            if with_proba:
                eweight += "\t1"*self.class_number
            cdtfile.write(eweight + "\n")
            # write classes
            for class_idx in range(self.class_number):
                cluster = self.df[self.df["main-class"]==class_idx]
                col_names = ["gid", "name1", "name2", "gweight"]
                col_names += self.experiment_names
                if with_proba:
                    col_names += ["prob-class-{}"
                                  .format(i) for i in range(self.class_number)]
                cdtfile.write(cluster.to_csv(sep="\t",
                                             columns=col_names,
                                             index=False,
                                             header=False,
                                             na_rep=""))
                # add spacer between clusters
                for dummy in range(1, 6):
                    cdtfile.write("GENE{:04d}-{:03.0f}S\n"
                                  .format(dummy, class_idx))


    @handle_error
    def write_cluster_stats(self):
        """
        Writing cluster stat file

        Mean and standard deviation values per experiment
        """
        # count number of unique classes
        class_max = self.df['main-class'].nunique()
        with open('clust_stat.tsv', 'w') as statfile:
            # write headers
            headers = ["cluster"] \
                    + self.experiment_names
            statfile.write("{}\n".format("\t".join(headers)))
            # write classes
            for class_idx in range(class_max):
                cluster = self.df[self.df["main-class"]==class_idx]
                row_mean = ["cluster{:03.0f}mean".format(class_idx)]
                row_std  = ["cluster{:03.0f}std".format(class_idx)]
                for exp in self.experiment_names:
                    row_mean.append("{:.3f}".format(cluster.mean()[exp]))
                    row_std.append("{:.3f}".format(cluster.std()[exp]))
                statfile.write("\t".join(row_mean)+"\n")
                statfile.write("\t".join(row_std)+"\n")


    @handle_error
    def wrap_outputs(self):
        """
        Wrap results into a ziped file
        """
        t = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        zipname = "{}-autoclass-clust.zip".format(t)
        with zipfile.ZipFile(zipname, "w") as outputzip:
            outputzip.write("clust.cdt")
            outputzip.write("clust_withprobs.cdt")
            outputzip.write("clust_stat.tsv")
        return zipname
