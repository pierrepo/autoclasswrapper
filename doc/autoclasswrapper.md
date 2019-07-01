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
