---
title: 'AutoClassWrapper: a Python wrapper for AutoClass C classification'
tags:
- python
- autoclass
- Bayesian
- proteomics
- clustering
authors:
- name: Jean-Michel Camadro
  orcid: 0000-0002-8549-2707
  affiliation: 1
- name: Pierre Poulain
  orcid: 0000-0003-4177-3619
  affiliation: 1
affiliations:
- name: Mitochondria, Metals and Oxidative Stress group, Institut Jacques Monod, UMR 7592, Univ. Paris Diderot, CNRS, Sorbonne Paris Cité, France.
  index: 1
date: 8 March 2019
bibliography: paper.bib
---


# Background

Data clustering or classification is widely used in many scientific fields and is often the very first step into exploratory data analysis.

In 1996, the Ames Research Center at NASA has developed AutoClass [@cheeseman1996,  @stutz1996], an unsupervised Bayesian classification system, and its implementation in C, AutoClass C. The purpose of the Bayesian methodology is to find the classification that fits the data with the highest probability. The AutoClass algorithm is very efficient, notably in its ability to automatically find the best number of classes (or clusters) and to handle missing data. AutoClass can handle both real (numerical) and discrete values. It has been successful in classifying data as diverse as infrared spectra of stars [@goebel1989], protein structures [@hunder1992], introns from human DNA sequences [@cheeseman1996], Landsat satellites images [@cheeseman1996], body pattern in the common cuttlefish [@crook2002], patterns between rich and poor countries [@ardic2006], network traffic [@erman2006], or catchments in the Australian landscape [@anguswebb2007]. In proteomics and genomics, where thousands of proteins or genes are detected at once, the need for data classification is even more crucial. To this aim, AutoClass@IJM [@achcar2009], a web server that utilizes AutoClass C, has been published few years ago to make Bayesian classification more accessible (see for instance results from [@simpson2011, @leger2015, @elliott2018]).


# Overview

The AutoClassWrapper library is a Python wrapper for AutoClass C. It aims to ease the usage of AutoClass C and offers:

- Data preparation. User input data must be formatted as tab-separated values (TSV) files. They are quality checked with the pandas library [@mckinney2010] and converted into suitable parameter files for AutoClass C.

- Results extraction. AutoClass C output files are processed into more usable formats, such as clustered data (CDT) file for further visualization in Java Treeview [@saldanha2004] or TSV file for analysis with R, Python or any spreadsheet software.

For all classes, descriptive statistics of numerical features are produced. An additional hierarchical clustering is performed on output classes and provides, through a dendrogram, a convenient way to assess proximity between classes.

AutoClassWrapper has been implemented with good practices in software development in mind [@jimenez2017, @taschuk2017]:

- version control repository on GitHub (https://github.com/pierrepo/autoclasswrapper),
- open-source license (BSD-3-Clause),
- continuous integration through tests,
- and documentation (https://autoclasswrapper.readthedocs.io/en/latest/).

AutoClassWrapper is available in the Python Package Index (PyPI). All versions of the software are archived in the Zenodo repository (https://doi.org/10.5281/zenodo.2527058) and in the Software Heritage archive (https://archive.softwareheritage.org/swh:1:dir:f888c9ca0a59d12e33ab16ba14d814c96c3648cd/).


# References
