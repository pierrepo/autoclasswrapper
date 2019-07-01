Welcome to AutoClassWrapper's documentation!
============================================

**Version** |release|


AutoClass is an unsupervised Bayesian classification system.

AutoClass C is an implementation of the AutoClass algorithm developed by the NASA in 1995.

AutoClassWrapper is a Python wrapper to ease the use of Autoclass C.


If you want to install AutoClassWrapper, use:

.. code-block:: bash

    $ pip install seq-to-first-iso 

you will also need AutoClass C:

.. code-block:: bash

    $ wget https://ti.arc.nasa.gov/m/project/autoclass/autoclass-c-3-3-6.tar.gz
    $ tar zxvf autoclass-c-3-3-6.tar.gz
    $ rm -f autoclass-c-3-3-6.tar.gz
    $ export PATH=$PATH:$(pwd)/autoclass-c

    # if you use a 64-bit operating system,
    # you also need to install the standard 32-bit C libraries:
    $ sudo apt-get install -y libc6-i386


User manual
===========
.. toctree::
    :maxdepth: 2

    autoclasswrapper


Tutorial
========
.. toctree::
    :maxdepth: 2

    notebooks/demo


Reference manual
================
.. toctree::
    :maxdepth: 2

    api/input
    api/run 
    api/output 
    api/tools




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`


