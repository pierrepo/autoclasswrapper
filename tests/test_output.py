import sys
import os
import shutil
import filecmp

import pytest

sys.path.insert(0,os.getcwd())
import autoclasswrapper as wrapper

here = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(here, "test_data")

target_root_name = "sample-3-classes-real-location"

@pytest.fixture(scope='session')
def tmp_dir(tmpdir_factory):
    """Create temp dir and cd in it
    """
    tmpd = tmpdir_factory.mktemp("output")
    os.chdir(str(tmpd))
    for ext in (".tsv", ".case-data-1"):
        shutil.copy2(os.path.join(data_dir, target_root_name + ext), str(tmpd))

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

    def test_extract_results(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        assert "Found 600 cases classified in 3 classes" in caplog.text
        assert res.stats["main-class"].nunique() == 3
        assert res.stats.shape == (600, 5)

    def test_aggregate_input_data(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        assert "Aggregating input data" in caplog.text
        assert os.path.isfile(res.root_out_name+".tsv")

    def test_write_cdt(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_cdt()
        assert os.path.isfile(res.root_out_name+".cdt")

    def test_write_cdt_with_proba(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_cdt(with_proba=True)
        assert os.path.isfile(res.root_out_name + "_withprobs.cdt")
        #reference_file = os.path.join(data_dir, target_root_name + "_out_withprobs.cdt")
        #assert filecmp.cmp(reference_file, res.root_out_name+"_withprobs.cdt")

    def test_write_cluster_stats(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_cluster_stats()
        assert os.path.isfile(res.root_out_name + "_stats.tsv")

    def test_write_dendrogram(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_dendrogram()
        assert os.path.isfile(res.root_out_name + "_dendrogram.png")
