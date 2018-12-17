"""autoclasswrapper: Python wrapper for AutoClass clustering.

Utilities.
"""

import logging
import shutil
import subprocess

log = logging.getLogger(__name__)


def search_autoclass_in_path():
    """Search if AutoClass C executable is in PATH.

    Returns
    -------
    str
        Path to Autoclass C binary.

    """
    autoclass_path = shutil.which("autoclass")
    if autoclass_path:
        log.info("AutoClass C executable found in {}".format(autoclass_path))
    else:
        log.error("AutoClass C executable not found in path!")
    return autoclass_path


def get_autoclass_version():
    """Output AutoClass C version.

    Returns
    -------
    version : str
        Autoclass version

    """
    version = ""
    if search_autoclass_in_path():
        version = subprocess.check_output(["autoclass"])
        version = version.decode("utf8").strip()
        log.info("AutoClass C version: {}".format(version))
    return version
