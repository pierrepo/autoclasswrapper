# AutoClass algorithm and context

AutoClass is an unsupervised Bayesian classification system developed at the NASA Ames Research Center in 1991 by [Hanson, Stutz and Cheeseman](https://ti.arc.nasa.gov/m/project/autoclass/tr-fia-90-12-7-01.ps). This algorithm has many interesting features:

- The number of classes are determined automatically.
- Missing values are supported.
- Discret and real values can be mixed.
- For all classified objects, the class membership probability is provided.

[AutoClass C](https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/) is the implementation of the AutoClass algorithm in C. It has been developed by Cheeseman and Stutz in 1996. AutoClass C has been successful in classifying data as diverse as infrared spectra of stars, protein structures, introns from human DNA sequences, Landsat satellites images, body pattern in the common cuttlefish, patterns between rich and poor countries, network traffic, or catchments in the Australian landscape. In proteomics and genomics, where thousands of proteins or genes are detected at once, AutoClass C has been proven to produce insightful results.

However, AutoClass C user interface isn't very friendly and requires that data and parameters are input in a very precise way. To help user to prepare data, perform classification and analyze clusters, we developed AutoClassWrapper as a Python wrapper around AutoClass C.


# Installation

To install AutoClassWrapper, use `pip`:

```bash
$ pip install seq-to-first-iso 
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

# Quickstart

## Data preparation 

AutoClass C can handle different types of data:

- *real scalar*: numerical values bounded by 0. Example: length, weight, age...
- *real location*: numerical values, positive et negative. Example: position, microarray log ratio, elevation...
- *discrete*: qualitative data. Example: color, phenotype, name...

Each data type must be entered as **separate input file**.

AutoClass C handles very well missing data. Missing data must be represented by nothing (no `NA`, `?`, `None`...).

The usual workflow to prepare data is to instantiate an object from the class `Input()`:
```python
import autoclasswrapper as wrapper
clust = wrapper.Input()
```

then add as many datasets as wanted, usually one per different data types (*real scalar*, *real location* and *discrete*):

```python 
clust.add_input_data("example1.tsv", "real scalar")
clust.add_input_data("example2.tsv", "real location")
```

Prefered input data format is tab-separated values. User must provide the type of data. 

The default error on real values is 0.01. Error is relative for *real scalar* (0.01 means 1%) but absolute for *real location*.

The next step is then to prepare input data and generate input files required by AutoClass C:

```python
clust.prepare_input_data()
clust.create_db2_file()
clust.create_hd2_file()
clust.create_model_file()
clust.create_sparams_file()
clust.create_rparams_file()
```

## Classification / clustering 

Once input files are created, one can run AutoClass C:

```python
run = wrapper.Run()

# prepare script to run autoclass
run.create_run_file()

# run autoclass
run.run()
```

Note that, at this stage, AutoClass C must be installed and available in PATH (see installation section).

Depending on the size of dataset (number of lines and columns), the classification might take some time to run.


## Results analysis

Upon classification, one can output results in different formats:

- `.cdt`: cluster data (CDT) files can be open with [Java Treeview](http://jtreeview.sourceforge.net/)
- `.tsv`: Tab-separated values (TSV) file can be easily open and process with Microsoft Excel, R, Python...
- `_stats.tsv`: basic statistics for all classes
- `_dendrogram.png`: figure with a dendrogram showing relationship between classes

Note that the first class as number 1.

