import sys
import os

import pytest

sys.path.insert(0,'..')
import autoclasswrapper as wrapper

here = os.path.abspath(os.path.dirname(__file__))
dir_data = "test_data"

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
                           message="Expecting DuplicateColumnNameError"):
            ds.check_duplicate_col_names()

    def test_read_datafile(self, caplog):
        name = os.path.join(here, dir_data, "sample1.tsv")
        ds = wrapper.Dataset(name, "real location", error=0.01)
        ds.read_datafile()
        assert "10 rows and 4 columns" in caplog.text

class TestInputClass(object):
    """Test for the Input class
    """

    def test_init(self):
        clust = wrapper.Input()
        assert clust.root_name == "clust"
        assert clust.db2_missing_char == "?"
        assert clust.db2_separator_char == "\t"
        assert clust.tolerate_error == False

    def test_add_input_data(self):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name)

    def test_add_input_data_dup_col_names(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "input-dup-col.tsv")
        clust.add_input_data(name, "real location")
        assert "Found duplicate column names" in caplog.text

    def test_create_db2_file(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_db2_file()
        assert os.path.isfile("clust.db2")
        assert os.path.isfile("clust.tsv")

    def test_create_hd2_file(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_hd2_file()
        assert os.path.isfile("clust.hd2")

    def test_create_model_file(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_model_file()
        assert os.path.isfile("clust.model")

    def test_create_sparams_file(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_sparams_file()
        assert os.path.isfile("clust.s-params")

    def test_create_rparams_file(self):
        filename = "clust.r-params"
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

    def test_create_run_file(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_run_file()
        assert os.path.isfile("clust.sh")

    def test_print_files(self):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        clust.create_hd2_file()
        clust.create_model_file()
        clust.create_sparams_file()
        clust.create_rparams_file()
        clust.create_run_file()
        content = clust.print_files()
        assert "clust.hd2" in content
        assert "clust.model" in content
        assert "clust.s-params" in content
        assert "clust.r-params" in content
        assert "clust.sh" in content
