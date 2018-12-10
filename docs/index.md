# Autoclasswrapper  documentation

## Installation

`autoclasswrapper` is available for Python 3.x only.

```
$ python3 -m pip install --user autoclasswrapper
```

## Architecture

`autoclasswrapper` exposes 3 classes:

- `Input()` prepares datasets for AutoClass clustering   
- `Run()` performs actual clustering. :warning: AutoClass must be installed and available in PATH.
- `Output()` reads AutoClass output files, generates more useable files and computes basic statistics on generated classes.
