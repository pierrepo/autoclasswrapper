Autoclasswrapper  documentation
===============================

.. toctree::
   :maxdepth: 1

   installation
   demo
   api_reference

Architecture
------------

`autoclasswrapper` exposes 3 classes:

- `Input()` prepares datasets for AutoClass clustering
- `Run()` performs actual clustering. :warning: AutoClass must be installed and available in PATH.
- `Output()` reads AutoClass output files, generates more useable files and computes basic statistics on generated classes.
