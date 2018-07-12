import sys
import os

import pytest

sys.path.insert(0,os.getcwd())
import autoclasswrapper as wrapper

here = os.path.abspath(os.path.dirname(__file__))
dir_data = "test_data"


class TestOutputClass(object):
    """Test for the Output class
    """

    def test_init(self):
        res = wrapper.Output()
        assert res.root_in_name == "clust"
        assert res.root_out_name == "clust_out"
        assert res.tolerate_error == False
        assert res.case_number == 0
        assert res.class_number == 0
        assert res.df == None
        assert res.stats == None
        assert res.experiment_names == []

    def test_extract_results(self, caplog):
        root_name = os.path.join(here, dir_data, "sample-3-classes-real-scalar")
        res = wrapper.Output(root_name)
        res.extract_results()
        assert "Found 600 cases classified in 3 classes" in caplog.text
        assert res.stats["main-class"].nunique() == 3
        assert res.stats.shape == (600, 5)
