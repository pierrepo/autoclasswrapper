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
target_root_path = os.path.join(data_dir, target_root_name)

@pytest.fixture(scope='session')
def tmp_dir(tmpdir_factory):
    """Create temp dir, add files and cd in it

    Temp dir is in /tmp/pytest-of-$USER/pytest-XXX/
    Doc: https://docs.pytest.org/en/latest/tmpdir.html
    """
    tmpd = tmpdir_factory.mktemp("output")
    os.chdir(str(tmpd))
    for ext in (".tsv", ".case-data-1"):
        shutil.copy2(os.path.join(data_dir, target_root_name + ext), str(tmpd))
    print("Tests are in: {}".format(str(tmpd)))


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
        ref_file = target_root_path + "_out.tsv"
        assert filecmp.cmp(ref_file, res.root_out_name + ".tsv", shallow=False)

    def test_write_cdt(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_cdt()
        assert os.path.isfile(res.root_out_name+".cdt")
        ref_file = target_root_path + "_out.cdt"
        assert filecmp.cmp(ref_file, res.root_out_name + ".cdt", shallow=False)

    def test_write_cdt_with_proba(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_cdt(with_proba=True)
        assert os.path.isfile(res.root_out_name + "_withprobs.cdt")
        ref_file = target_root_path + "_out_withprobs.cdt"
        assert filecmp.cmp(ref_file,
                           res.root_out_name + "_withprobs.cdt",
                           shallow=False)

    def test_write_dendrogram_no_stats(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_dendrogram()
        statfile = res.root_out_name + "_stats.tsv"
        assert "Cannot find {}".format(statfile) in caplog.text

    def test_write_cluster_stats(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_class_stats()
        assert os.path.isfile(res.root_out_name + "_stats.tsv")
        ref_file = target_root_path + "_out_stats.tsv"
        assert filecmp.cmp(ref_file,
                           res.root_out_name + "_stats.tsv",
                           shallow=False)

    def test_write_dendrogram(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_dendrogram()
        assert os.path.isfile(res.root_out_name + "_dendrogram.png")

    def test_wrap_outputs(self, caplog, tmp_dir):
        res = wrapper.Output(target_root_name)
        res.extract_results()
        res.aggregate_input_data()
        res.write_cdt()
        res.write_cdt(with_proba=True)
        res.write_class_stats()
        res.write_dendrogram()
        zipname = res.wrap_outputs()
        assert os.path.isfile(zipname)
