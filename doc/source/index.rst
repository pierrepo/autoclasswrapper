Autoclasswrapper documentation
==============================

Version 1.2.0

.. toctree::
   :maxdepth: 1

   installation
   demo
   api_reference

Architecture
------------

`autoclasswrapper` exposes 3 classes:

- `Input()` prepares datasets for AutoClass C clustering
- `Run()` performs actual clustering.
    AutoClass C binary must be installed and available in PATH.
- `Output()` reads AutoClass C output files, generates more useable files and computes basic statistics on generated classes.
