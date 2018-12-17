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
    # create fake autoclass binary and add it to PATH
    autoclass_bin = "autoclass"
    open(autoclass_bin, "a").close()
    os.chmod(autoclass_bin, 766)
    os.environ["PATH"] = os.getcwd() + ":" + os.environ["PATH"]
    wrapper.search_autoclass_in_path()
    assert "AutoClass C executable found in" in caplog.text


def test_get_autoclass_version(caplog):
    wrapper.get_autoclass_version()
    assert "AUTOCLASS" in caplog.text
