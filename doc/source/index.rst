AutoClassWrapper documentation
==============================

Version 1.3.0

.. toctree::
   :maxdepth: 1

   installation
   demo
   api_reference

Architecture
------------

``autoclasswrapper`` exposes 3 classes:

- ``Input()`` prepares datasets for AutoClass C clustering.
- ``Run()`` performs actual clustering. `AutoClass C <https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/>`_ binary must be installed and available in ``PATH``.
- ``Output()`` reads AutoClass C output files, generates more useable files and computes basic statistics on generated classes.
