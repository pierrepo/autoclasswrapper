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

class TestRunClass(object):
    """Test for the Run class
    """
    def test_create_run_file(self, caplog):
        clust = wrapper.Input()
        name = os.path.join(here, dir_data, "sample1.tsv")
        clust.add_input_data(name, "real location")
        clust.merge_dataframes()
        run = wrapper.Run()
        run.create_run_file()
        assert os.path.isfile("clust.sh")
