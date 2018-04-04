import sys
import os

import pytest

sys.path.insert(0,'..')
import autoclasswrapper as wrapper

here = os.path.abspath(os.path.dirname(__file__))
dir_data = "test_data"

class TestDatasetClass(object):
    """
    Tests for the Dataset class
    """

    def test_init(self):
        ds = wrapper.Dataset()
        assert ds.input_file == ""
        assert ds.df == None
        assert ds.column_meta == {}
        assert ds.separator == "\t"

    def test_check_duplicate_col_names(self):
        ds = wrapper.Dataset()
        ds.input_file = os.path.join(here, dir_data, "input-dup-col.tsv")
        with pytest.raises(wrapper.DuplicateColumnNameError,
                           message="Expecting DuplicateColumnNameError"):
            ds.check_duplicate_col_names()


class TestInputClass(object):
    """
    Test for the Input class
    """

    def test_init(self):
        clust = wrapper.Input()
        assert clust.inputfolder == ""
        assert clust.missing_encoding == "?"
        assert clust.separator == "\t"
        assert clust.tolerate_error == False

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
