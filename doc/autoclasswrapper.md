# AutoClass algorithm and context

AutoClass is an unsupervised Bayesian classification system developed at the NASA Ames Research Center in 1991 by [Hanson, Stutz and Cheeseman](https://ti.arc.nasa.gov/m/project/autoclass/tr-fia-90-12-7-01.ps). This algorithm has many interesting features:

- The number of classes are determined automatically.
- Missing values are supported.
- Discret and real values can be mixed.
- For all classified objects, the class membership probability is provided.

[AutoClass C](https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/) is the implementation of the AutoClass algorithm in C. It has been developed by Cheeseman and Stutz in 1996. AutoClass C has been successful in classifying data as diverse as infrared spectra of stars, protein structures, introns from human DNA sequences, Landsat satellites images, body pattern in the common cuttlefish, patterns between rich and poor countries, network traffic, or catchments in the Australian landscape. In proteomics and genomics, where thousands of proteins or genes are detected at once, AutoClass C has been proven to produce insightful results.

However, AutoClass C user interface isn't very friendly and requires that data and parameters are input in a very precise way. To help user to prepare input data, perform classification and analyze output clusters, we developed AutoClassWrapper as a Python wrapper around AutoClass C.


# Installation

To install AutoClassWrapper, use `pip`:

```bash
$ python3 -m pip install autoclasswrapper
```

you will also need AutoClass C:

```
$ wget https://ti.arc.nasa.gov/m/project/autoclass/autoclass-c-3-3-6.tar.gz
$ tar zxvf autoclass-c-3-3-6.tar.gz
$ rm -f autoclass-c-3-3-6.tar.gz
$ export PATH=$PATH:$(pwd)/autoclass-c

# if you use a 64-bit operating system,
# you also need to install the standard 32-bit C libraries:
$ sudo apt-get install -y libc6-i386
```

# Data preparation 

AutoClass C can handle 3 different types of data:

- *real scalar*: numerical values bounded by 0. Examples: length, weight, age...
- *real location*: numerical values, positive and negative. Examples: position, microarray log ratio, elevation...
- *discrete*: qualitative data. Examples: color, phenotype, name...

Each data type must be entered in **separate input file** (one for each type).

AutoClass C handles missing data. Missing data must be represented by nothing (no `NA`, `?`, `None`, `NULL`...).

The usual workflow to prepare data is to instantiate an object from the `Input()` class:
```python
import autoclasswrapper as wrapper
clust = wrapper.Input()
```

then add as many datasets as wanted, usually one per different data types:

```python 
clust.add_input_data("example1.tsv", "real scalar")
clust.add_input_data("example2.tsv", "real location")
```

Input data format is [tab-separated](https://en.wikipedia.org/wiki/Tab-separated_values) values. Together with the name of the input file, user must provide the type of data (either `real scalar`, `real location` or `discrete`). 

The default error on real values is 0.01. Error is relative for *real scalar* values (0.01 means 1%) but absolute for *real location* values. There is no error for *discrete* values. For *real scalar* and *real location* values, custom error can be defined with the `input_error` parameter of the `.add_input_data()` method.

The next step is to prepare input data and generate input files required by AutoClass C:

```python
clust.prepare_input_data()
clust.create_db2_file()
clust.create_hd2_file()
clust.create_model_file()
clust.create_sparams_file()
clust.create_rparams_file()
```

All this commands are compulsory and will create several parameter files in the current directory.


# Classification / clustering 

Once input files are created, one can build Bash run script and actually run AutoClass C:

```python
import autoclasswrapper as wrapper
run = wrapper.Run()
run.create_run_file()
run.run()
```

At this stage, AutoClass C must be installed and available in PATH (see installation section).

The Bash script that run AutoClass C runs it actually twice. The first time to perform the classification (clustering). The second  time to build a report from the raw results.

The Bash script that run AutoClass C is loaded itself with the `nohup` command. This means that the only way to stop this script is by killing it!

Depending on the size of the datasets (number of lines and columns), the classification might take some time to run (from few seconds to several hours). By default, the maximum running time is 3600 seconds (1 hour). This setting can be modified with the `max_duration` parameter of the `.create_sparams_file()` method.


# Results analysis

Upon classification, results are ouput in different formats:

- `.cdt`: cluster data (CDT) files can be open with [Java Treeview](http://jtreeview.sourceforge.net/)
- `.tsv`: Tab-separated values (TSV) file can be easily open and process with Microsoft Excel, R, Python...
- `_stats.tsv`: basic statistics for all classes
- `_dendrogram.png`: figure with a dendrogram showing relationship between classes

Note that the first class has number **1** (not 0).

```python
import autoclasswrapper as wrapper
results = wrapper.Output()
results.extract_results()
results.aggregate_input_data()
results.write_cdt()
results.write_cdt(with_proba=True)
results.write_class_stats()
results.write_dendrogram()
```

The `.tsv` files contains:

- The initial dataset.
- A `main-class` column that gives the class with the highest probability.
- A `main-class-proba` column that contains the actual probability value (between 0.0 and 1.0) of the most probable class.
- `class-x-proba` columns (with `x` being a class number) that provide the probability to belong the `x` class.
 