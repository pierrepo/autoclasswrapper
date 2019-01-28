# AutoClassWrapper: a Python wrapper for AutoClass C classification

[![License: BSD](https://img.shields.io/badge/License-BSD-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)   [![autoclasswrapper version on PyPI](https://badge.fury.io/py/autoclasswrapper.svg)](https://pypi.python.org/pypi/autoclasswrapper)   [![Build Status](https://travis-ci.org/pierrepo/autoclasswrapper.svg?branch=master)](https://travis-ci.org/pierrepo/autoclasswrapper)
[![Documentation Status](https://readthedocs.org/projects/autoclasswrapper/badge/?version=latest)](https://autoclasswrapper.readthedocs.io/en/latest/?badge=latest)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2527059.svg)](https://doi.org/10.5281/zenodo.2527059)


AutoClass is an unsupervised Bayesian classification system.

[AutoClass C](https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/) is an implementation of the AutoClass algorithm made by the NASA.

AutoClassWrapper is a Python wrapper to ease the use of Autoclass C.


## Installation and dependencies

Dependencies:

- **Python 3.6** or above
- Python libraries: NumPy, Pandas, Scipy, matplotlib, chardet

AutoClassWrapper is available through the Python Package Index ([PyPI](https://pypi.org/)):

```
$ python3 -m pip install --user autoclasswrapper
```
or
```
$ pipenv --three
$ pipenv install autoclasswrapper
```


## Documentation

Documentation is available on [ReadTheDocs](https://autoclasswrapper.readthedocs.io/en/latest/)


## License

AutoClassWrapper is free software made available under the BSD 3-clause license. For more details see the [LICENSE](LICENSE.txt) file.


## Contributing

If you want to report a bug, request a feature, or propose an improvement use the [GitHub issue system](https://github.com/pierrepo/autoclasswrapper/issues/).

Please, see also the [CONTRIBUTING](CONTRIBUTING.md) file.

Note that this project is released with a [Contributor Code of
Conduct](http://contributor-covenant.org/). By participating in this project you
agree to abide by its terms. See the [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) file.
