# AutoClassWrapper: a Python wrapper for AutoClass C classification

[![License: BSD](https://img.shields.io/badge/License-BSD-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)   [![autoclasswrapper version on PyPI](https://badge.fury.io/py/autoclasswrapper.svg)](https://pypi.python.org/pypi/autoclasswrapper)   [![Build Status](https://travis-ci.org/pierrepo/autoclasswrapper.svg?branch=master)](https://travis-ci.org/pierrepo/autoclasswrapper)
[![Documentation Status](https://readthedocs.org/projects/autoclasswrapper/badge/?version=latest)](https://autoclasswrapper.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pierrepo/autoclasswrapper/master?filepath=notebooks)
[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2527058.svg)](https://doi.org/10.5281/zenodo.2527058)
[![JOSS DOI](http://joss.theoj.org/papers/10.21105/joss.01390/status.svg)](https://doi.org/10.21105/joss.01390)


AutoClass is an unsupervised Bayesian classification system.

[AutoClass C](https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/) is an implementation of the AutoClass algorithm made by the NASA.

AutoClassWrapper is a Python wrapper to ease the use of Autoclass C.


## Installation and dependencies


### AutoClass C installation 

AutoClass C can be found [here](https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/). The installation process can be achieved with the following commands:
```
$ wget https://ti.arc.nasa.gov/m/project/autoclass/autoclass-c-3-3-6.tar.gz
$ tar zxvf autoclass-c-3-3-6.tar.gz
$ rm -f autoclass-c-3-3-6.tar.gz
$ export PATH=$PATH:$(pwd)/autoclass-c
```

Please note that is you are running a 64-bit operating system, you will also need to install the standard 32-bit libraries. For instance, on a Debian/Ubuntu-like system:
```
$ sudo apt-get install -y libc6-i386
```


### AutoClassWrapper installation 

Dependencies:

- **Python 3.6** or above
- Python libraries: NumPy, Pandas, Scipy, matplotlib, chardet

AutoClassWrapper is available through the Python Package Index ([PyPI](https://pypi.org/)):

```
$ python3 -m pip install autoclasswrapper
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
