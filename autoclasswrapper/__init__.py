import logging
log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
# log_f = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#                           "%Y-%m-%d %H:%M:%S")
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)
log.setLevel(logging.DEBUG)

from .input import Input, Dataset, DuplicateColumnNameError
from .output import Output
