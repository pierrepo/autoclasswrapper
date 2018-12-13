import sys
import os

AUTHORS = [u'Pierre Poulain']

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'nbsphinx',
]


# The suffix of source filenames.
source_suffix = ['.rst', '.ipynb']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'autoclasswrapper'
copyright = u'2018, Pierre Poulain'

# The short X.Y.Z version.
import autoclasswrapper
version = autoclasswrapper.__version__
# The full version, including alpha/beta/rc tags.
release = autoclasswrapper.__version__


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['**.ipynb_checkpoints']


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
