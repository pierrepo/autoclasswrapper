Demo
====

You will find demo dataset and script in the `demo` directory of the project.

To get the project, you can either clone it:

.. code-block:: bash

    $ git clone https://github.com/pierrepo/autoclasswrapper.git autoclasswrapper


or download it:

.. code-block:: bash

    $ wget https://github.com/pierrepo/autoclasswrapper/archive/master.zip
    $ unzip master.zip
    $ mv autoclasswrapper-master/ autoclasswrapper


Input step
----------

From the `demo` directory, you can run the input step:

.. code-block:: bash

    $ python3 demo_input.py
    2018-12-11 00:03:29 INFO     Reading data file 'sample-3-classes-real-location.tsv' as 'real location' with error 0.01
    2018-12-11 00:03:29 INFO     Detected encoding: ascii
    2018-12-11 00:03:29 INFO     Found 600 rows and 3 columns
    2018-12-11 00:03:29 DEBUG    Checking column names
    2018-12-11 00:03:29 DEBUG    Index name 'Name'
    2018-12-11 00:03:29 DEBUG    Column name 'x'
    2018-12-11 00:03:29 DEBUG    Column name 'y'
    2018-12-11 00:03:29 INFO     Checking data format
    2018-12-11 00:03:29 INFO     Column 'x'
    count    600.000000
    mean      -0.010474
    std        4.113536
    min       -6.146841
    50%       -0.067324
    max        6.028697
    2018-12-11 00:03:29 INFO     Column 'y'
    count    600.000000
    mean      -0.026946
    std        0.498592
    min       -1.369286
    50%       -0.019496
    max        1.664992
    2018-12-11 00:03:29 INFO     Final dataframe has 600 lines and 3 columns
    2018-12-11 00:03:29 INFO     Searching for missing values
    2018-12-11 00:03:29 INFO     No missing values found
    2018-12-11 00:03:29 INFO     Writing clust.db2 file
    2018-12-11 00:03:29 INFO     If any, missing values will be encoded as '?'
    2018-12-11 00:03:29 DEBUG    Writing clust.tsv file [for later use]
    2018-12-11 00:03:29 INFO     Writing .hd2 file
    2018-12-11 00:03:29 INFO     Writing .model file
    2018-12-11 00:03:29 INFO     Writing .s-params file
    2018-12-11 00:03:29 INFO     Writing .r-params file


Run step
--------

Autoclass setup
```````````````

For this step, you need a valid autoclass installation. This can be quickly achieved with:

.. code-block:: bash

    $ wget https://ti.arc.nasa.gov/m/project/autoclass/autoclass-c-3-3-6.tar.gz
    $ tar zxvf autoclass-c-3-3-6.tar.gz
    $ rm -f autoclass-c-3-3-6.tar.gz
    $ export PATH=$PATH:$(pwd)/autoclass-c

On a 64-bit operating system, you will also need 32-bit C librairies:

.. code-block:: bash

    $ sudo apt-get install -y lib32z1


Autoclass run
`````````````

From the `demo` directory, you can run the run step:

.. code-block:: bash

    python3 demo_run.py
    2018-12-11 00:13:03 INFO     autoclass executable found in /home/pierre/.soft/bin/autoclass
    2018-12-11 00:13:03 INFO     Writing run file
    2018-12-11 00:13:03 INFO     Running clustering...
    nohup: les entrées sont ignorées et la sortie est ajoutée à 'nohup.out'


The test dataset is very small, the clustering should take few seconds.


Output step
-----------

Once Autoclass has ran, from the `demo` directory, you can run the output step:

.. code-block:: bash

    python3 demo_output.py
    2018-12-11 00:16:35 INFO     Extracting autoclass results
    2018-12-11 00:16:35 INFO     Found 600 cases classified in 5 classes
    2018-12-11 00:16:36 INFO     Aggregating input data
    2018-12-11 00:16:36 INFO     Writing clust + probs .tsv file
    2018-12-11 00:16:36 INFO     Writing .cdt file
    2018-12-11 00:16:36 INFO     Writing .cdt file (with probs)
    2018-12-11 00:16:36 INFO     Writing cluster stats
    2018-12-11 00:16:36 INFO     Writing dendrogram
    2018-12-11 00:16:36 INFO     clust_out.tsv added to zip file
    2018-12-11 00:16:36 INFO     clust_out.cdt added to zip file
    2018-12-11 00:16:36 INFO     clust_out_withprobs.cdt added to zip file
    2018-12-11 00:16:36 INFO     clust_out_stats.tsv added to zip file
    2018-12-11 00:16:36 INFO     clust_out_dendrogram.png added to zip file
