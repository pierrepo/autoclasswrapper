"""autoclasswrapper: Python wrapper for AutoClass C classification.

Input files and parameters
"""

import logging
import os
import re

import chardet
import pandas as pd

log = logging.getLogger(__name__)


def raise_on_duplicates(input_list):
    """Verify duplicated values in a list.

    Parameters
    ----------
    input_list : list of strings
        List of column names.

    Raises
    ------
    DuplicateColumnNameError : exception
        If there is a duplicated element in the input list.

    """
    if len(input_list) != len(set(input_list)):
        col_names = " ".join(["'{}'".format(name) for name in input_list])
        raise DuplicateColumnNameError("Found duplicate column names:\n"
                                       f"{col_names}\n"
                                       "Please clean your header")


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
    r"""AutoClass C input files and parameters.

    Parameters
    ----------
    root_name : string, optional (default "autoclass")
        Root name to generate input files for AutoClass C.
        Example: "autoclass" will lead to "autoclass.db2",
        "autoclass.model", "autoclass.s-params"...
    db2_separator_char : string, optional (default: "\t")
        Character used to separate columns of data in AutoClass C db2 file.
    db2_missing_char : string, optional (default: "?")
        Character used to encode missing data in AutoClass C db2 file.
    tolerate_error : bool, optional (default: False)
        If True, countinue generation of AutoClass C input files even if an
        error is encounter.
        If False, stop at first error.

    Attributes
    ----------
    had_error : bool (defaut False)
        Set to True if an error has been found in the generation of AutoClass C
        input files.
    input_datasets : list of Dataset() objects
        List of all input Datasets.
    full_dataset : Dataset() object
        Final Dataset used by AutoClass C.

    """

    def __init__(self,
                 root_name="autoclass",
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
                       input_error=0.01,
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
        input_error : float, optional (default: 0.01)
            Input error value.
        input_separator_char : string, optional (default: "\t")
            Character used to separate columns of data in input file.
        input_missing_char : string, optional (default: "")
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
    def prepare_input_data(self):
        """Prepare input data.

        - Create a final dataframe.
        - Merge datasets if multiple inputs.

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
            log.info("Preparing input data")
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
        log.info(f"Final dataframe has {nrows} lines and {ncols+1} columns")
        self.full_dataset.search_missing_values()

    @handle_error
    def create_db2_file(self):
        """Create .db2 file (AutoClass C data).

        Also save all data into a .tsv file for later user.
        """
        db2_name = self.root_name + ".db2"
        tsv_name = self.root_name + ".tsv"
        log.info(f"Writing {db2_name} file")
        log.info("If any, missing values will be encoded"
                 f" as '{self.db2_missing_char}'")
        self.full_dataset.df.to_csv(db2_name,
                                    header=False,
                                    sep=self.db2_separator_char,
                                    na_rep=self.db2_missing_char)
        log.debug(f"Writing {tsv_name} file [for later use]")
        self.full_dataset.df.to_csv(tsv_name,
                                    header=True,
                                    sep="\t",
                                    na_rep="")

    @handle_error
    def create_hd2_file(self):
        """Create .hd2 file (AutoClass C data descriptions)."""
        log.info("Writing .hd2 file")
        hd2_name = self.root_name + ".hd2"
        column_names = self.full_dataset.df.columns
        with open(hd2_name, "w") as hd2:
            hd2.write("num_db2_format_defs 2\n")
            hd2.write("\n")
            # get number of columns + index
            hd2.write(f"number_of_attributes {len(column_names)+1}\n")
            hd2.write(f"separator_char '{self.db2_separator_char}'\n")
            hd2.write("\n")
            # write first columns (protein/gene names)
            hd2.write(f'0 dummy nil "{self.full_dataset.df.index.name}"\n')
            for idx, name in enumerate(column_names):
                meta = self.full_dataset.column_meta[name]
                if meta["type"] == "real scalar":
                    # by default minimum value is set to 0.0
                    assert self.full_dataset.df.min()[idx] >= 0.0, \
                           f"min value for {name} shoud be >= 0.0"
                    hd2.write(f'{idx+1} real scalar "{name}" '
                              f'zero_point 0.0 rel_error {meta["error"]}\n'
                              )
                if meta["type"] == "real location":
                    hd2.write(f'{idx+1} real location "{name}" '
                              f'error {meta["error"]}\n'
                              )
                if meta["type"] == "discrete":
                    hd2.write(f'{idx+1} discrete nominal "{name}" '
                              f'range {self.full_dataset.df[name].nunique()}\n'
                              )

    @handle_error
    def create_model_file(self):
        """Create .model file (AutoClass C data models).

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
            model.write(f"model_index 0 {models_count}\n")
            model.write("ignore 0\n")
            if real_values_normals:
                model.write("single_normal_cn "
                            f"{' '.join(real_values_normals)}\n")
            if real_values_missing:
                model.write("single_normal_cm "
                            f"{' '.join(real_values_missing)}\n")
            if multinomial_values:
                model.write("single_multinomial "
                            f"{' '.join(multinomial_values)}\n")

    @handle_error
    def create_sparams_file(self,
                            max_duration=3600,
                            max_n_tries=200,
                            max_cycles=1000,
                            start_j_list=[2, 3, 5, 7, 10, 15, 25, 35,
                                          45, 55, 65, 75, 85, 95, 105],
                            reproducible_run=False):
        """Create .s-params file (AutoClass C search parameters).

        Parameters
        ----------
        max_duration : int, optional (default: 3600)
            Maximum time (in seconds) for the AutoClass C simulation.
            If set max_duration = 0, simulation will run with NO time limit
            For more details, see AutoClass C documentation:
            file search-c.text, lines 493-495
        max_n_tries : int, optional (default: 200)
            Number of trials to run.
            For more details, see AutoClass C documentation:
            file search-c.text, lines 403-404
        max_cycles : int, optional (default: 1000)
            Max number of cycles per trial.
            This is maximum that may not be reached.
            For more details, see AutoClass C documentation:
            file search-c.text, lines 316-317
        start_j_list : list of int, optional (default: [2, 3, 5, 7, 10, 15, 25, 35,
                                                        45, 55, 65, 75, 85, 95, 105])
            Initial guesses of the number of clusters
            Autoclass default: 2, 3, 5, 7, 10, 15, 25
            For more details, see AutoClass C documentation:
            file search-c.text, line 332
        reproducible_run : boolean, optional (default: False)
            If set to True, define parameters to obtain reproducible run.
            According to AutoClass C developers: "These parameter settings are 
            for testing *only* -- they should not be utilized for normal AutoClass runs."

            - randomize_random_p = false
                Random seed is set to 1 (instead of the usual current time)
            - start_fn_type = "block"
                Instead of "random"
            - min_report_period = value greater than duration of run

            For more details, see AutoClass C documentation:

            - file search-c.text, line 678
            - file search-c.text, line 565
            - file search-c.text, line 525

        """
        log.info("Writing .s-params file")
        sparams_name = self.root_name + ".s-params"
        with open(sparams_name, "w") as sparams:
            sparams.write("screen_output_p = false \n")
            sparams.write("break_on_warnings_p = false \n")
            sparams.write("force_new_search_p = true \n")
            sparams.write(f"max_duration = {max_duration}\n")
            sparams.write(f"max_n_tries = {max_n_tries}\n")
            sparams.write(f"max_cycles = {max_cycles}\n")
            starters = [str(j) for j in start_j_list]
            sparams.write(f"start_j_list = {', '.join(starters)}\n")
            if reproducible_run is True:
                sparams.write("randomize_random_p = false\n")
                sparams.write('start_fn_type = "block"\n')
                sparams.write(f"min_report_period = {max_duration*2}\n")

    @handle_error
    def create_rparams_file(self):
        """Create .r-params file (AutoClass C report parameters)."""
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
            Contain all AutoClass C parameter files concatenated.

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
        "merged" is a special case corresponding to merged datasets.
    error : float, optional (default: 0.01)
        Value of error on data.
    separator_char : string, optional (defaut: "\t")
        Character used to separate columns of data in input file.
    missing_char : string, optional (default: "")
        Character used to encode missing data in input file.


    Attributes
    ----------
    input_file : string (defaut: "")
        Name of the file to read data from.
    separator_char : string (defaut: "\t")
        Character used to separate columns of data in input file.
    df : Pandas dataframe (default: None)
        Pandas dataframe that contains all data.
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
        """Instantiate object."""
        self.input_file = input_file
        self.data_type = data_type
        self.error = error
        self.separator_char = separator_char
        self.missing_char = missing_char
        self.df = None
        self.column_meta = {}
        # verify data type
        assert self.data_type in \
            ["real scalar", "real location", "discrete", "merged"], \
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
        msg = (f"Reading data file '{self.input_file}' "
               f"as '{self.data_type}'")
        if self.data_type in ["real scalar", "real location"]:
            msg += f" with error {self.error}"
        log.info(msg)
        # check for duplicate column names
        self.check_duplicate_col_names()
        # find encoding
        encoding = self.guess_encoding()
        log.info(f"Detected encoding: {encoding}")
        # load data
        self.df = pd.read_csv(self.input_file,
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
        log.info(f"Found {nrows} rows and {ncols+1} columns")

    def clean_column_names(self):
        """Clean column names.

        Allowed characters are:

        - `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
        - `abcdefghijklmnopqrstuvwxyz`
        - `0123456789`
        - `.` (dot)
        - `+` (plus signe)
        - `-` (minus signe)
        - `_` (underscore)

        Unauthorized characters are replaced by '_'
        """
        # regex = re.compile('[^A-Za-z0-9 ._+-]+')
        regex = re.compile("[^A-Za-z0-9._+-]+")
        log.debug("Checking column names")
        # check index column name first
        col_name = self.df.index.name
        col_name_new = regex.sub("_", col_name)
        if col_name_new != col_name:
            self.df.index.name = col_name_new
            log.warning(f"Column '{col_name}' renamed to '{col_name_new}'")
        # then other column names
        for col_name in self.df.columns:
            col_name_new = regex.sub("_", col_name)
            if col_name_new != col_name:
                self.df.rename(columns={col_name: col_name_new}, inplace=True)
                log.warning(f"Column '{col_name}' renamed to '{col_name_new}'")
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
            if self.column_meta[col]["type"] in ["real scalar",
                                                 "real location"]:
                try:
                    self.df[col].astype("float64")
                    stats = (f"Column '{col}'\n"
                             + self.df[col]
                                   .describe(percentiles=[])
                                   .to_string()
                             )
                    for line in stats.split("\n"):
                        log.info(line)
                    log.info("---")
                except Exception as e:
                    raise CastFloat64Error(
                        f"Cannot cast column '{col}' to float\n"
                        f"{str(e)}\n"
                        "Check your input file!")
            if self.column_meta[col]['type'] == "discrete":
                log.info(f"Column '{col}': "
                         f"{self.df[col].nunique()} different values"
                         )

    def search_missing_values(self):
        """Search for missing values."""
        log.info("Searching for missing values")
        columns_with_missing = self.df.columns[self.df.isnull().any()].tolist()
        if columns_with_missing:
            for col in columns_with_missing:
                self.column_meta[col]["missing"] = True
                log.warning(f"Missing values found in column: {col}")
        else:
            log.info("No missing values found")
