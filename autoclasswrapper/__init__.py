"""autoclasswrapper: Python wrapper for AutoClass clustering."""

__version__ = "0.1.14"
__copyright__ = "Copyright 2018 Pierre Poulain"

import logging

from .input import (Input,
                    Dataset,
                    raise_on_duplicates,
                    DuplicateColumnNameError,
                    CastFloat64Error)
from .output import Output
from .run import search_autoclass_in_path, Run

log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)
log.setLevel(logging.DEBUG)
