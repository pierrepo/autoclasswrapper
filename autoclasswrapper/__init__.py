import logging
log = logging.getLogger(__name__)
log_h = logging.StreamHandler()
log_f = logging.Formatter('%(asctime)s :: %(levelname)-8s :: %(message)s',
                          "%Y-%m-%d %H:%M")
log_h.setFormatter(log_f)
log.addHandler(log_h)
log.setLevel(logging.DEBUG)

from .input import Input, Dataset, DuplicateColumnNameError
from .output import Output
