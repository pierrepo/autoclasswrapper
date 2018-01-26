import os
import random
import subprocess
import re
import logging
import numpy as np
import pandas as pd

#import utilities

logging.basicConfig(level=logging.DEBUG)



def raise_on_duplicates(input_list):
    """
    Verify if a list as duplicated values.

    Raised DuplicateColumnName exception if this is the cas.
    """
    if len(input_list) != len(set(input_list)):
        raise DuplicateColumnName(
                ("Found duplicate column names:\n"
                 "{}\n"
                 "Please clean your header"
                ).format(" ".join(input_list)) )


class CastFloat64(Exception):
    """
    Exception raised when data column cannot be casted to float64
    """

    def __init__(self, message):
        self.message = message


class DuplicateColumnName(Exception):
    """
    Exception raised when column names are identical
    """

    def __init__(self, message):
        self.message = message

class Process():
    """
    Class to handle autoclass input files and parameters
    """

    def __init__(self, inputfolder='', missing_encoding="?", tolerate_error=False):
        """
        Object instanciation
        """
        self.inputfolder = inputfolder
        self.missing_encoding = missing_encoding

        self.input_datasets = []
        self.full_dataset = Dataset()

        self.tolerate_error = tolerate_error
        self.had_error = False


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
                        logging.error(line)
                    self.had_error = True
        return try_function


    @handle_error
    def change_working_dir(self):
        """
        change working dir
        """
        logging.info("Changing working directory")
        os.chdir(self.inputfolder)


    @handle_error
    def add_input_data(self, input_file, input_type, input_error):
        """
        Add input data for clustering
        """
        dataset = Dataset()
        logging.info("Reading data file {}".format(input_file))
        dataset.read_datafile(input_file, input_type, input_error)
        dataset.clean_column_names()
        dataset.check_data_type()
        self.input_datasets.append(dataset)


    @handle_error
    def merge_dataframes(self):
        """
        Merge input dataframes from datasets

        Dataframes are merged based on an 'outer' join
        https://pandas.pydata.org/pandas-docs/stable/merging.html
        - all lines are kept
        - missing data might appear
        """
        # merge dataframes and column meta data
        if len(self.input_datasets) == 1:
            self.full_dataset = self.input_datasets[0]
        else:
            logging.info("Merging input data")
            df_lst = []
            for dataset in self.input_datasets:
                df_lst.append(dataset.df)
                self.full_dataset.column_meta = \
                {**self.full_dataset.column_meta, **dataset.column_meta}
            self.full_dataset.df = pd.concat(df_lst, axis=1, join="outer")
        # check for identical column names
        raise_on_duplicates(self.full_dataset.df.columns)

        nrows, ncols = self.full_dataset.df.shape
        logging.info("Final dataframe has {} lines and {} columns"
                     .format(nrows, ncols+1))
        self.full_dataset.search_missing_values()


    @handle_error
    def create_db2_file(self, filename="clust"):
        """
        Create .db2 file
        """
        db2_name = filename + ".db2"
        tsv_name = filename + ".tsv"
        logging.info("Writing {} file".format(db2_name))
        logging.info("If any, missing values will be encoded as '{}'"
                     .format(self.missing_encoding))
        self.full_dataset.df.to_csv("clust.db2",
                                    header=False,
                                    sep="\t",
                                    na_rep=self.missing_encoding)
        logging.debug("Writing {} file [for later use]".format(tsv_name))
        self.full_dataset.df.to_csv("clust.tsv",
                                    header=True,
                                    sep="\t",
                                    na_rep="")


    @handle_error
    def create_hd2_file(self):
        """
        create .hd2 file
        """
        logging.info("Writing .hd2 file")
        error_type = "rel_error"
        error_value = self.error
        with open("clust.hd2", "w") as hd2:
            hd2.write("num_db2_format_defs {}\n".format(2))
            hd2.write("\n")
            # get number of columns + index
            hd2.write("number_of_attributes {}\n".format(self.ncols+1))
            hd2.write("separator_char '{}'\n".format("\t"))
            hd2.write("\n")
            # write first columns (protein/gene names)
            hd2.write('0 dummy nil "{}"\n'.format(self.df.index.name))
            for col_id in range(self.ncols):
                hd2.write('{} real scalar "{}" zero_point {} {} {}\n'
                          .format(col_id+1, self.df.columns[col_id], self.df.min()[col_id], error_type, error_value))


    @handle_error
    def create_model_file(self):
        """
        Create .model file
        """
        logging.info("Writing .model file")
        real_values_normals = ""
        real_values_missing = ""
        multinomial_values = ""
        for index, column in enumerate(self.columns):
            print(column)
            if column.type in ['scalar', 'linear']:
                if not column.missing:
                    real_values_normals += '{} '.format(index+1)
                else:
                    real_values_missing += '{} '.format(index+1)
            if column.type == 'discrete':
                multinomial_values += '{} '.format(index+1)
        # count number of different models
        model_count = 1
        for model in [real_values_normals, real_values_missing, multinomial_values]:
            if model:
                model_count += 1
        # write model file
        with open("clust.model", "w") as model:
            model.write("model_index 0 {}\n".format(model_count))
            model.write("ignore 0\n")
            if real_values_normals:
                model.write("single_normal_cn {}\n".format(real_values_normals))
            if real_values_missing:
                model.write("single_normal_cm {}\n".format(real_values_missing))
            if multinomial_values:
                model.write("single_multinomial {}\n".format(multinomial_values))


    @handle_error
    def create_sparams_file(self):
        """
        create  .s-params file
        """
        logging.info("Writing .s-params file")
        with open("clust.s-params", "w") as sparams:
            sparams.write('screen_output_p = false \n')
            sparams.write('break_on_warnings_p = false \n')
            sparams.write('force_new_search_p = true \n')

            # max_duration
            # When > 0, specifies the maximum number of seconds to run.
            # When = 0, allows run to continue until otherwise halted.
            # doc in search-c.text, lines 493-495
            # default value: max_duration = 0
            # max_duration set to 3600 sec. (1 hour)
            sparams.write('max_duration = 3600 \n')

            # max_n_tries
            # max number of trials
            # doc in search-c.text, lines 403-404
            # default value: max_n_tries = 200
            sparams.write('max_n_tries = 1000 \n')

            # max_cycles
            # max number of cycles per trial
            # doc in search-c.text, lines 316-317
            # default value: max_cyles = 200
            sparams.write('max_cycles = 1000 \n')

            # start_j_list
            # initial guess of the number of clusters
            # doc in search-c.text, line 332
            # default values: 2, 3, 5, 7, 10, 15, 25
            sparams.write('start_j_list = 2, 3, 5, 7, 10, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105 \n')


    @handle_error
    def create_rparams_file(self):
        """
        create .r-params file

        try those parameters:
        report_mode = "data"
        comment_data_headers_p = true
        """
        logging.info("Writing .r-params file")
        with open("clust.r-params", "w") as rparams:
            rparams.write('xref_class_report_att_list = 0, 1, 2 \n')


    @handle_error
    def create_run_file(self):
        """
        Create .sh file
        """
        logging.info("Writing run file")
        with open('run_autoclass.sh', 'w') as runfile:
            runfile.write("../autoclass -search clust.db2 clust.hd2 clust.model clust.s-params \n")
            runfile.write("../autoclass -reports clust.results-bin clust.search clust.r-params \n")


    @handle_error
    def prepare_input_files(self):
        """
        Prepare input and parameters files
        """
        logging.info("Preparing data and parameters files")
        self.change_working_dir()
        self.create_db2_file()
        self.create_hd2_file()
        self.create_model_file()
        self.create_sparams_file()
        self.create_rparams_file()
        self.create_run_file()


    @handle_error
    def run(self):
        """
        Run autoclass
        """
        logging.info("Running clustering...")
        proc = subprocess.Popen(['bash', 'run_autoclass.sh', self.inputfolder])
        print(" ".join(proc.args))
        return True

    '''
    @handle_error
    def set_password(self, password_length):
        """
        Output access token for user

        Token is 8 characters long and always start with the 'T' letter
        """
        logging.info("{} / writing access file".format(self.inputfolder))
        token = utilities.create_random_string(password_length-1)
        token = 'P' + token
        with open('access', 'w') as accessfile:
            accessfile.write(token)
        return token
    '''

    @handle_error
    def print_files(self):
        """
        Print generated files
        """
        content = ""
        for name in ('clust.hd2', 'clust.model', 'clust.s-params', 'clust.r-params', 'run_autoclass.sh'):
            if os.path.exists(name):
                content += "\n"
                content += "--------------------------------------------------------------------------\n"
                content += "{}\n".format(name)
                content += "--------------------------------------------------------------------------\n"
                with open(name, 'r') as param_file:
                    content += "".join( param_file.readlines() )
        return content


        @handle_error
        def format_results(self):
            """
            Format results for end user
            """
            case_name = 'clust.case-data-1'
            case_id = []
            case_class = []
            case_prob = []
            with open(case_name, 'r') as case_file:
                for line in case_file:
                    if not line:
                        continue
                    if line.startswith('#') or line.startswith('DATA'):
                        continue
                    items = line.split()
                    case_id.append( items[0] )
                    case_class.append( items[1] )
                    case_prob.append( items[2] )
            self.df = pd.read_table(self.inputfile, sep='\t', header=0, index_col=0)
            self.nrows, self.ncols = self.df.shape
            if (self.nrows != len(case_class)) or (self.nrows != len(case_prob)):
                raise('Number of rows != number of cases!')
            self.df['cluster_class'] = case_class
            self.df['cluster_prob'] = case_prob
            self.df.sort(['cluster_class'], ascending=[True], inplace=True)


class Dataset():
    """
    Class to handle autoclass data files
    """


    def __init__(self):
        """
        Object instantiation
        """
        # filename of input_file
        self.input_file = ""
        # Pandas dataframe with data
        self.df = None
        # Column meta data: data type, error, missing values
        self.column_meta = {}


    def load(self):
        """
        Load data
        """
        self.read_datafile()
        self.clean_column_names()
        self.check_data_type()
        self.check_missing_values()



    def check_duplicate_col_names(self, input_file):
        """
        Check duplicate column clean_column_names
        """
        with open(input_file) as f_in:
            header = f_in.readline().strip().split("\t")
            raise_on_duplicates(header)


    def read_datafile(self, input_file='', data_type='', error=0.0):
        """
        Read data file as pandas dataframe

        Header is on first row (header=0)
        Gene/protein/orf names are on first column (index_col=0)
        """
        # verify data type
        assert data_type in ['real_scalar', 'real_location', 'discrete'], \
               ("data_type in {} should be: "
                "'real_scalar', 'real_location' or 'discrete'"
                .format(input_file))
        # check for duplicate column names
        self.input_file = input_file
        self.check_duplicate_col_names(input_file)
        # load data
        self.df = pd.read_table(input_file, sep='\t', header=0, index_col=0)
        nrows, ncols = self.df.shape
        # save column meta data (data type, error, missing values)
        for col in self.df.columns:
            meta = {'type': data_type,
                    'error': error,
                    'missing': False}
            self.column_meta[col] = meta
        logging.info("Found {} rows and {} columns"
                     .format(nrows, ncols+1))


    def clean_column_names(self):
        """
        Cleanup column names
        """
        regex = re.compile('[^A-Za-z0-9 .-]+')
        logging.debug("Checking column names")
        # check index column name first
        col_name = self.df.index.name
        col_name_new = regex.sub("_", col_name)
        if col_name_new != col_name:
            self.df.index.name = col_name_new
            logging.warning("Column '{}' renamed to '{}'"
                            .format(col_name, col_name_new))
        # then other column names
        for col_name in self.df.columns:
            col_name_new = regex.sub("_", col_name)
            if col_name_new != col_name:
                self.df.rename(columns={col_name: col_name_new}, inplace=True)
                logging.warning("Column '{}' renamed to '{}'"
                                .format(col_name, col_name_new))
                # update column meta data
                self.column_meta[col_name_new] = self.column_meta.pop(col_name)
        # print all columns names
        logging.debug("Index name {}'".format(self.df.index.name))
        for name in self.df.columns:
            logging.debug("Column name '{}'".format(name))


    def check_data_type(self):
        """
        Check data type
        """
        logging.info("Checking data format")
        for col in self.df.columns:
            if self.column_meta[col] in ['real_scalar', 'real_location']:
                try:
                    self.df[col].astype('float64')
                    logging.info("Column '{}'\n".format(col)
                                 +self.df[col].describe(percentiles=[]).to_string())
                except:
                    raise CastFloat64(("Cannot cast column '{}' to float\n"
                                       "Check your input file!").format(col)
                                     )

    def search_missing_values(self):
        """
        Search for missing values
        """
        logging.info('Searching for missing values')
        columns_with_missing = self.df.columns[ self.df.isnull().any() ].tolist()
        if columns_with_missing:
            for col in columns_with_missing:
                self.column_meta[col]['missing'] = True
            logging.warning('Missing values found in columns: {}'
                            .format(" ".join(columns_with_missing)))
        else:
            logging.info('No missing values found')
