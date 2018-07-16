import sys
import os

import pytest

sys.path.insert(0, os.getcwd())
import autoclasswrapper as wrapper

here = os.path.abspath(os.path.dirname(__file__))
dir_data = "test_data"

@pytest.fixture(scope='session')
def tmp_dir(tmpdir_factory):
    """Create temp dir and cd in it
    """
    tmpd = tmpdir_factory.mktemp("run")
    os.chdir(str(tmpd))
    print("Tests are in: {}".format(str(tmpd)))


def test_search_autoclass_in_path(caplog, tmp_dir):
    # create fake autoclass binary add add it to PATH
    autoclass_bin = "autoclass"
    open(autoclass_bin, "a").close()
    os.chmod(autoclass_bin, 766)
    os.environ["PATH"] = os.getcwd() + ":" + os.environ["PATH"]
    wrapper.search_autoclass_in_path()
    assert "autoclass executable found in" in caplog.text

class TestRunClass(object):
    """Test for the Run class
    """
    def test_create_run_file(self, caplog, tmp_dir):
        run = wrapper.Run()
        run.create_run_file()
        assert os.path.isfile("clust.sh")

    def test_create_run_file_test(self, caplog, tmp_dir):
        run = wrapper.Run()
        run.create_run_file_test()
        assert os.path.isfile("clust.sh")
