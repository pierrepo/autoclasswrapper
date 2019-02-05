import sys
import os

import pytest

sys.path.insert(0,os.getcwd())
import autoclasswrapper as wrapper

here = os.path.abspath(os.path.dirname(__file__))
dir_data = "test_data"

@pytest.fixture(scope='session')
def tmp_dir(tmpdir_factory):
    """Create temp dir and cd in it
    """
    tmpd = tmpdir_factory.mktemp("input")
    os.chdir(str(tmpd))

def test_raise_on_duplicates(caplog):
    with pytest.raises(wrapper.DuplicateColumnNameError,
                       match="Found duplicate column names"):
        wrapper.raise_on_duplicates(["A", "B", "B"])


class TestDatasetClass(object):
    """Tests for the Dataset class
    """

    def test_init(self):
        ds = wrapper.Dataset("", "merged")
        assert ds.input_file == ""
        assert ds.data_type == "merged"
        assert ds.error == None
        assert ds.df == None
        assert ds.column_meta == {}
        assert ds.separator_char == "\t"
        assert ds.missing_char == ""

    def test_check_duplicate_col_names(self):
        ds = wrapper.Dataset("", "merged")
        ds.input_file = os.path.join(here, dir_data, "input-dup-col.tsv")
        with pytest.raises(wrapper.DuplicateColumnNameError,
                           match="Found duplicate column names"):
            ds.check_duplicate_col_names()

    def test_read_datafile(self, caplog):
        name = os.path.join(here, dir_data, "sample-real-location.tsv")
        ds = wrapper.Dataset(name, "real location", error=0.01)
        ds.read_datafile()
        assert "10 rows and 4 columns" in caplog.text

    def test_check_data_type_real_location_OK(self, caplog):
        name = os.path.join(here, dir_data, "sample-real-location.tsv")
        ds = wrapper.Dataset(name, "real location", error=0.01)
        ds.read_datafile()
        ds.check_data_type()
        assert "10 rows and 4 columns" in caplog.text
        assert "Column 'colA'" in caplog.text
        assert "Column 'colB'" in caplog.text
        assert "Column 'colC'" in caplog.text

    def test_check_data_type_real_location_not_OK(self, caplog):
        name = os.path.join(here, dir_data, "sample-discrete.tsv")
        ds = wrapper.Dataset(name, "real location", error=0.01)
        ds.read_datafile()
        assert "10 rows and 3 columns" in caplog.text
        with pytest.raises(wrapper.CastFloat64Error,
                           match="could not convert string to float"):
            ds.check_data_type()

    def test_check_data_type_discrete_OK(self, caplog):
        name = os.path.join(here, dir_data, "sample-discrete.tsv")
        ds = wrapper.Dataset(name, "discrete")
        ds.read_datafile()
        ds.check_data_type()
        assert "10 rows and 3 columns" in caplog.text
        assert "Column 'colD': 2 different values" in caplog.text
        assert "Column 'colE': 3 different values" in caplog.text

    def test_search_missing_values(self, caplog):
        name = os.path.join(here, dir_data, "sample-missing-values.tsv")
        ds = wrapper.Dataset(name, "real location", error=0.01)
        ds.read_datafile()
        ds.search_missing_values()
        assert ("WARNING  Missing values found in columns:"
                " colI colJ") in caplog.text

    def test_clean_column_names(self, caplog):
        name = os.path.join(here, dir_data, "sample-column-names.tsv")
        ds = wrapper.Dataset(name, "real location", error=0.01)
        ds.read_datafile()
        ds.clean_column_names()
        assert "Column 'gene(name)' renamed to 'gene_name_'" in caplog.text
        assert "Column 'coléèà' renamed to 'col_'" in caplog.text
        assert "Column 'col[]()/' renamed to 'col_'" in caplog.text



class TestInputClass(object):
    """Test for the Input class
    """

    def test_init(self, tmp_dir):
        clust = wrapper.Input()
        assert clust.root_name == "autoclass"
        assert clust.db2_missing_char == "?"
        assert clust.db2_separator_char == "\t"
        assert clust.tolerate_error == False

    def test_add_input_data(self):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name)

    def test_add_input_data_dup_col_names(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "input-dup-col.tsv")
        clust.add_input_data(name, "real location")
        assert "Found duplicate column names" in caplog.text

    def test_merge_data(self, caplog):
        clust = wrapper.Input()
        name1 = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name1, "real location")
        name2 = os.path.join(here, dir_data, "sample-discrete.tsv")
        clust.add_input_data(name2, "discrete")
        name3 = os.path.join(here, dir_data, "sample-real-scalar.tsv")
        clust.add_input_data(name3, "real scalar")
        clust.merge_dataframes()
        print(caplog.text)
        assert "Final dataframe has 10 lines and 8 columns" in caplog.text

    def test_create_db2_file(self, caplog):
        clust = wrapper.Input()
        name1 = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name1, "real location")
        name2 = os.path.join(here, dir_data, "sample-discrete.tsv")
        clust.add_input_data(name2, "discrete")
        name3 = os.path.join(here, dir_data, "sample-real-scalar.tsv")
        clust.add_input_data(name3, "real scalar")
        clust.merge_dataframes()
        clust.create_db2_file()
        assert os.path.isfile("autoclass.db2")
        assert os.path.isfile("autoclass.tsv")

    def test_create_hd2_file(self, caplog):
        clust = wrapper.Input()
        name1 = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name1, "real location")
        name2 = os.path.join(here, dir_data, "sample-discrete.tsv")
        clust.add_input_data(name2, "discrete")
        name3 = os.path.join(here, dir_data, "sample-real-scalar.tsv")
        clust.add_input_data(name3, "real scalar")
        clust.merge_dataframes()
        clust.create_hd2_file()
        assert os.path.isfile("autoclass.hd2")

    def test_create_model_file(self, caplog):
        clust = wrapper.Input()
        name1 = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name1, "real location")
        name2 = os.path.join(here, dir_data, "sample-discrete.tsv")
        clust.add_input_data(name2, "discrete")
        name3 = os.path.join(here, dir_data, "sample-real-scalar.tsv")
        clust.add_input_data(name3, "real scalar")
        name4 = os.path.join(here, dir_data, "sample-missing-values.tsv")
        clust.add_input_data(name4, "real location")
        clust.merge_dataframes()
        clust.create_model_file()
        assert os.path.isfile("autoclass.model")

    def test_create_sparams_file(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_sparams_file()
        assert os.path.isfile("autoclass.s-params")

    def test_create_sparams_file_repro_run(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_sparams_file(reproducible_run=True)
        assert os.path.isfile("autoclass.s-params")
        f_content = open("autoclass.s-params", "r").read()
        assert "randomize_random_p = false" in f_content
        assert 'start_fn_type = "block"' in f_content

    def test_create_rparams_file(self):
        filename = "autoclass.r-params"
        clust = wrapper.Input()
        clust.create_rparams_file()
        assert os.path.isfile(filename)
        content_ref = ""
        filename_ref = os.path.join(here, "test_data", filename)
        with open(filename_ref , "r") as f:
            content_ref = f.read()
        content = ""
        with open(filename , "r") as f:
            content = f.read()
        assert content == content_ref

    def test_print_files(self):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample-real-location.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_hd2_file()
        clust.create_model_file()
        clust.create_sparams_file()
        clust.create_rparams_file()
        content = clust.print_files()
        assert "autoclass.hd2" in content
        assert "autoclass.model" in content
        assert "autoclass.s-params" in content
        assert "autoclass.r-params" in content
