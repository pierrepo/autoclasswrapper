**Dev**

**1.4.0**
- Print columuns with missing values one column per line
- Embed column stats in logging output

**1.3.0**
- Redirect run ouput to log files
- Use f-strings

**1.2.0**
- Handle error while checking for autoclass version
- Fix missing margin in dendrogram picture

**1.1.0**
- Rewrite write_dendrogram() method
- Rename marker files (autoclass_run_*) in snake_case

**1.0.0**
- Jump to major release

**0.2.2**
- Remove wrap method for results
- Update list of authorized characters in column names

**0.2.1**
- Move function utilities to tools.py
- Change defaut filename to 'autoclass'

**0.2.0**
- Fix error decorator for Sphinx doc generation
- Use 'class' (instead of 'cluster') for consistency
- Move get_autoclass_version() out of Run() class
- Create file marker upon autoclass run success/failure

**0.1.14**
- update missing dependencies in setup.cfg
- improve PEP 8 and PEP 257 compliance
- add documentation (Sphinx)

**0.1.13**
- print Exception content for check_data_type()
- output class probability for every gene/protein
- simplify the calculation of cluster stats
- class/cluster numbering starts at 1 (0-based in autoclass output)
- add dendrogram of classes
- add reproducible run option (test only)
- add tests for Input() class
- add tests for Output() class
- add tests for Run() class

**0.1.12**
- update write_cluster_stats() methods with mean/std column
- output data+clusters in clust_data.tsv

**0.1.11**
- add nohup while running autoclass script

**0.1.10**
- search_autoclass_in_path() returns the PATH

**0.1.9**
- check autoclass-c executable is in PATH
- building and running script are in Run() class

**0.1.8**
- add env in Popen()

**0.1.7**
- add missing dependencies

**0.1.6**
- move distribution package to bdist_wheel

**0.1.5**
- move config options to setup.cfg

**0.1.4**
- add MANIFEST.in

**0.1.3**
- remove tests from Python package

**0.1.2**
- add Markdown support for README description
