"""autoclasswrapper: Python wrapper for AutoClass clustering.

Input files and parameters
"""

import logging
import os
import re

import chardet
import pandas as pd

log = logging.getLogger(__name__)


def raise_on_duplicates(input_list):
    """Verify if a list as duplicated values.

    Parameters
    ----------
    input_list : list of strings
        List of column names.

    Raises
    ----------
    DuplicateColumnNameError : exception
        If there is a duplicated element in the input list.

    """
    if len(input_list) != len(set(input_list)):
        col_names = ["'{}'".format(name) for name in input_list]
        raise DuplicateColumnNameError(
            ("Found duplicate column names:\n"
             "{}\n"
             "Please clean your header"
             ).format(" ".join(col_names)))


class DuplicateColumnNameError(Exception):
    """Exception raised when column names are identical."""

    def __init__(self, message):
        """Instantiate object."""
        self.message = message


class CastFloat64Error(Exception):
    """Exception raised when data column cannot be casted to float64 type."""

    def __init__(self, message):
        """Instantiate object."""
        self.message = message


class Input():
    r"""Autoclass input files and parameters.

    Parameters
    ----------
    root_name : string (default "clust")
        Root name to generate input files for autoclass.
        Example: "clust" will lead to "clust.db2", "clust.model"...
    db2_separator_char : string (default: "\t")
        Character used to separate columns of data in autoclass db2 file.
    db2_missing_char : string (default: "?")
        Character used to encode missing data in autoclass db2 file.
    tolerate_error : bool (default: False)
        If True, countinue generation of autoclass input files even if an
        error is encounter.
        If False, stop at first error.

    Attributes
    ----------
    had_error : bool (defaut False)
        Set to True if an error has been found in the generation of autoclass
        input files.
    input_datasets : list of Dataset() objects
        List of all input Datasets.
    full_dataset : Dataset() object
        Final Dataset used by autoclass.

    """

    def __init__(self,
                 root_name="clust",
                 db2_separator_char="\t",
                 db2_missing_char="?",
                 tolerate_error=False):
        """Instantiate object."""
        self.root_name = root_name
        self.db2_separator_char = db2_separator_char
        self.db2_missing_char = db2_missing_char
        self.tolerate_error = tolerate_error
        self.had_error = False
        self.input_datasets = []
        self.full_dataset = Dataset("", "merged")

    def handle_error(f):
        """Handle error during data parsing and formating.

        Function decorator.

        Parameters
        ----------
        f : function

        Returns
        -------
        try_function : function wrapped into error handler

        """
        def try_function(self, *args, **kwargs):
            if self.tolerate_error or not self.had_error:
                try:
                    return f(self, *args, **kwargs)
                except Exception as e:
                    for line in str(e).split('\n'):
                        log.error(line)
                    self.had_error = True
        try_function.__name__ = f.__name__
        try_function.__doc__ = f.__doc__
        return try_function

    @handle_error
    def add_input_data(self,
                       input_file,
                       input_type,
                       input_error=None,
                       input_separator_char="\t",
                       input_missing_char=""):
        r"""Read input data file and append to list of datasets.

        Parameters
        ----------
        input_file : string
            Name of the data file to read.
        input_type : string
            Type of data contained in input file.
            Either "real scalar", "real location" or "discrete"
        input_error : float (default: None)
            Input error value.
        input_separator_char : string (default: "\t")
            Character used to separate columns of data in input file.
        input_missing_char : string (default: "")
            Character used to encode missing data in input file.

        """
        dataset = Dataset(input_file,
                          input_type,
                          input_error,
                          input_separator_char,
                          input_missing_char)
        dataset.read_datafile()
        dataset.clean_column_names()
        dataset.check_data_type()
        self.input_datasets.append(dataset)

    @handle_error
    def merge_dataframes(self):
        """Merge input dataframes from datasets.

        Notes
        -----
        Dataframes are merged based on an 'outer' join
        https://pandas.pydata.org/pandas-docs/stable/merging.html
        - all lines are kept
        - missing data might appear

        """
        if len(self.input_datasets) == 1:
            self.full_dataset = self.input_datasets[0]
        else:
            log.info("Merging input data")
            df_lst = []
            for dataset in self.input_datasets:
                df_lst.append(dataset.df)
                # 'merge' column meta data
                self.full_dataset.column_meta = \
                    {**self.full_dataset.column_meta, **dataset.column_meta}
            # merge dataframes
            self.full_dataset.df = pd.concat(df_lst, axis=1, join="outer")
        # check for identical column names
        raise_on_duplicates(self.full_dataset.df.columns)

        nrows, ncols = self.full_dataset.df.shape
        log.info("Final dataframe has {} lines and {} columns"
                 .format(nrows, ncols+1))
        self.full_dataset.search_missing_values()

    @handle_error
    def create_db2_file(self):
        """Create .db2 file (data).

        Also save all data into a .tsv file for later user.
        """
        db2_name = self.root_name + ".db2"
        tsv_name = self.root_name + ".tsv"
        log.info("Writing {} file".format(db2_name))
        log.info("If any, missing values will be encoded as '{}'"
                 .format(self.db2_missing_char))
        self.full_dataset.df.to_csv(db2_name,
                                    header=False,
                                    sep=self.db2_separator_char,
                                    na_rep=self.db2_missing_char)
        log.debug("Writing {} file [for later use]".format(tsv_name))
        self.full_dataset.df.to_csv(tsv_name,
                                    header=True,
                                    sep="\t",
                                    na_rep="")

    @handle_error
    def create_hd2_file(self):
        """Create .hd2 file (Autoclass data descriptions)."""
        log.info("Writing .hd2 file")
        hd2_name = self.root_name + ".hd2"
        column_names = self.full_dataset.df.columns
        with open(hd2_name, "w") as hd2:
            hd2.write("num_db2_format_defs {}\n".format(2))
            hd2.write("\n")
            # get number of columns + index
            hd2.write("number_of_attributes {}\n".format(len(column_names)+1))
            hd2.write("separator_char '{}'\n".format(self.db2_separator_char))
            hd2.write("\n")
            # write first columns (protein/gene names)
            hd2.write('0 dummy nil "{}"\n'
                      .format(self.full_dataset.df.index.name))
            for idx, name in enumerate(column_names):
                meta = self.full_dataset.column_meta[name]
                if meta["type"] == "real scalar":
                    # by default minimum value is set to 0.0
                    assert self.full_dataset.df.min()[idx] >= 0.0, \
                           "min value for {} shoud be >= 0.0".format(name)
                    hd2.write(('{} real scalar "{}" '
                               'zero_point 0.0 rel_error {}\n')
                              .format(idx+1,
                                      name,
                                      meta["error"])
                              )
                if meta["type"] == "real location":
                    hd2.write('{} real location "{}" error {}\n'
                              .format(idx+1,
                                      name,
                                      meta["error"])
                              )
                if meta["type"] == "discrete":
                    hd2.write('{} discrete nominal "{}" range {}\n'
                              .format(idx+1,
                                      name,
                                      self.full_dataset.df[name].nunique())
                              )

    @handle_error
    def create_model_file(self):
        """Create .model file (Autoclass data models).

        Choice of model based on data type and missing values
        """
        log.info("Writing .model file")
        model_name = self.root_name + ".model"
        # available models:
        real_values_normals = []
        real_values_missing = []
        multinomial_values = []
        # assign column data to models
        for col_idx, col_name in enumerate(self.full_dataset.df.columns):
            meta = self.full_dataset.column_meta[col_name]
            if meta['type'] in ['real scalar', 'real location']:
                if not meta['missing']:
                    real_values_normals.append(str(col_idx+1))
                else:
                    real_values_missing.append(str(col_idx+1))
            if meta['type'] == 'discrete':
                multinomial_values.append(str(col_idx+1))
        # count number of different models used
        # the first model is the one with labels (first column)
        models_count = 1
        for model in [real_values_normals,
                      real_values_missing,
                      multinomial_values]:
            if model:
                models_count += 1
        # write model file
        with open(model_name, "w") as model:
            model.write("model_index 0 {}\n".format(models_count))
            model.write("ignore 0\n")
            if real_values_normals:
                model.write("single_normal_cn {}\n"
                            .format(" ".join(real_values_normals)))
            if real_values_missing:
                model.write("single_normal_cm {}\n"
                            .format(" ".join(real_values_missing)))
            if multinomial_values:
                model.write("single_multinomial {}\n"
                            .format(" ".join(multinomial_values)))

    @handle_error
    def create_sparams_file(self,
                            max_duration=3600,
                            max_n_tries=200,
                            max_cycles=1000,
                            start_j_list=[2, 3, 5, 7, 10, 15, 25, 35,
                                          45, 55, 65, 75, 85, 95, 105],
                            reproducible_run=False):
        """Create .s-params file (Autoclass search parameters).

        Parameters
        ----------
        max_duration : int (default: 3600)
            Maximum time (in seconds) for the autoclass simulation.
            If set max_duration = 0, simulation will run with NO time limit
            For more details, see autoclass documentation:
            file search-c.text, lines 493-495
        max_n_tries : int (default: 200)
            Number of trials to run.
            For more details, see autoclass documentation:
            file search-c.text, lines 403-404
        max_cycles : int (default: 1000)
            Max number of cycles per trial.
            This is maximum that may not be reached.
            For more details, see autoclass documentation:
            file search-c.text, lines 316-317
        start_j_list : list of int (default: [2, 3, 5, 7, 10, 15, 25, 35,
                                             45, 55, 65, 75, 85, 95, 105])
            Initial guesses of the number of clusters
            Autoclass default: 2, 3, 5, 7, 10, 15, 25
            For more details, see autoclass documentation:
            file search-c.text, line 332
        reproducible_run : boolean (default: False)
            If set to True, define parameters to obtain reproducible run.
            This parameters are considered "for testing *only*" by autoclass-c
            and should NOT be used for production run.
            The following autoclass-c parameters are set:
            - randomize_random_p = false
                Random seed is set to 1 (instead of the usual current time)
            - start_fn_type = "block"
                Instead of "random"
            For more details, see autoclass documentation:
            file search-c.text, line 678
            file search-c.text, line 565
            file search-c.text, line 525

        """
        log.info("Writing .s-params file")
        sparams_name = self.root_name + ".s-params"
        with open(sparams_name, "w") as sparams:
            sparams.write("screen_output_p = false \n")
            sparams.write("break_on_warnings_p = false \n")
            sparams.write("force_new_search_p = true \n")
            sparams.write("max_duration = {}\n".format(max_duration))
            sparams.write("max_n_tries = {}\n".format(max_n_tries))
            sparams.write("max_cycles = {}\n".format(max_cycles))
            starters = [str(j) for j in start_j_list]
            sparams.write("start_j_list = {}\n".format(", ".join(starters)))
            if reproducible_run is True:
                sparams.write("randomize_random_p = false\n")
                sparams.write('start_fn_type = "block"\n')

    @handle_error
    def create_rparams_file(self):
        """Create .r-params file (Autoclass report parameters)."""
        log.info("Writing .r-params file")
        rparams_name = self.root_name + ".r-params"
        with open(rparams_name, "w") as rparams:
            rparams.write('xref_class_report_att_list = 0, 1, 2 \n')
            rparams.write('report_mode = "data" \n')
            rparams.write('comment_data_headers_p = true \n')

    @handle_error
    def print_files(self):
        """
        Print generated files.

        Debug usage.

        Returns
        -------
        content : string
            Contain all autoclass parameter files concatenated.

        """
        content = ""
        for extension in (".hd2", ".model", ".s-params", ".r-params"):
            name = self.root_name + extension
            if os.path.exists(name):
                content += "\n"
                content += "-" * 80 + "\n"
                content += "{}\n".format(name)
                content += "-" * 80 + "\n"
                with open(name, "r") as param_file:
                    content += "".join(param_file.readlines())
        return content


class Dataset():
    r"""Handle input data.

    Parameters
    ----------
    input_file : string (defaut: "")
        Name of the file to read data from.
    data_type : string (dafault: "")
        Type of data contained in input file.
        Either "real scalar", "real location", "discrete" or "merged"
        "merged" is special case corresponding to merged datasets.
    error : int (default: None)
        Value of error on data.
    separator_char : string (defaut: "\t")
        Character used to separate columns of data in input file.
    missing_char : string (default: "")
        Character used to encode missing data in input file.


    Attributes
    ----------
    input_file : string (defaut: "")
        Name of the file to read data from.
    separator_char : string (defaut: "\t")
        Character used to separate columns of data in input file.
    df : Pandas dataframe (default: None)
        All data are stored in a Pandas dataframe
    column_meta : dict (default: {})
        Dictionnary that contains metadata for each column.
        Keys are column names.
        Values are another dictionnary:
        {"type": data_type, "error": error, "missing": False}

    """

    def __init__(self,
                 input_file="",
                 data_type="",
                 error=None,
                 separator_char="\t",
                 missing_char=""):
        """Object instantiation."""
        self.input_file = input_file
        self.data_type = data_type
        self.error = error
        self.separator_char = separator_char
        self.missing_char = missing_char
        self.df = None
        self.column_meta = {}
        # verify data type
        assert self.data_type in \
            ['real scalar', 'real location', 'discrete', 'merged'], \
            ("data type in {} should be: "
             "'real scalar', 'real location' or 'discrete'"
             .format(self.input_file))

    def check_duplicate_col_names(self):
        """Check duplicate column names."""
        with open(self.input_file) as f_in:
            header = f_in.readline().strip().split(self.separator_char)
            raise_on_duplicates(header)

    def guess_encoding(self):
        """Guess input file encoding.

        Returns
        -------
         : string
            Type of encoding.

        """
        with open(self.input_file, 'rb') as f:
            enc_result = chardet.detect(f.read())
            return enc_result['encoding']

    def read_datafile(self):
        """Read data file as pandas dataframe.

        Header must be on the first row (header=0)
        Gene/protein/orf names must be on the first column (index_col=0)
        """
        msg = "Reading data file '{}' as '{}'".format(self.input_file,
                                                      self.data_type)
        if self.data_type in ['real scalar', 'real location']:
            msg += " with error {}".format(self.error)
        log.info(msg)
        # check for duplicate column names
        self.check_duplicate_col_names()
        # find encoding
        encoding = self.guess_encoding()
        log.info("Detected encoding: {}".format(encoding))
        # load data
        self.df = pd.read_table(self.input_file,
                                sep=self.separator_char,
                                header=0,
                                index_col=0,
                                encoding=encoding)
        nrows, ncols = self.df.shape
        # save column meta data (data type, error, missing values)
        for col in self.df.columns:
            meta = {"type": self.data_type,
                    "error": self.error,
                    "missing": False}
            self.column_meta[col] = meta
        log.info("Found {} rows and {} columns".format(nrows, ncols+1))

    def clean_column_names(self):
        """Clean column names.

        Replace unwanted characters by '_'
        """
        regex = re.compile('[^A-Za-z0-9 ._+-]+')
        log.debug("Checking column names")
        # check index column name first
        col_name = self.df.index.name
        col_name_new = regex.sub("_", col_name)
        if col_name_new != col_name:
            self.df.index.name = col_name_new
            log.warning("Column '{}' renamed to '{}'"
                        .format(col_name, col_name_new))
        # then other column names
        for col_name in self.df.columns:
            col_name_new = regex.sub("_", col_name)
            if col_name_new != col_name:
                self.df.rename(columns={col_name: col_name_new}, inplace=True)
                log.warning("Column '{}' renamed to '{}'"
                            .format(col_name, col_name_new))
                # update column meta data
                self.column_meta[col_name_new] = self.column_meta.pop(col_name)
        # print all columns names
        log.debug("Index name '{}'".format(self.df.index.name))
        for name in self.df.columns:
            log.debug("Column name '{}'".format(name))

    def check_data_type(self):
        """Check data type.

        Cast 'real scalar' and 'real location' to float64
        """
        log.info("Checking data format")
        for col in self.df.columns:
            if self.column_meta[col]['type'] in ['real scalar',
                                                 'real location']:
                try:
                    self.df[col].astype('float64')
                    log.info("Column '{}'\n".format(col)
                             + (self.df[col].describe(percentiles=[])
                                            .to_string())
                             )
                except Exception as e:
                    raise CastFloat64Error(("Cannot cast column '{}' "
                                            "to float\n"
                                            "{}\n"
                                            "Check your input file!"
                                            ).format(col, str(e))
                                           )
            if self.column_meta[col]['type'] == "discrete":
                log.info("Column '{}': {} different values"
                         .format(col, self.df[col].nunique())
                         )

    def search_missing_values(self):
        """Search for missing values."""
        log.info("Searching for missing values")
        columns_with_missing = self.df.columns[self.df.isnull().any()].tolist()
        if columns_with_missing:
            for col in columns_with_missing:
                self.column_meta[col]['missing'] = True
            log.warning("Missing values found in columns: '{}'"
                        .format(" ".join(columns_with_missing)))
        else:
            log.info("No missing values found")
