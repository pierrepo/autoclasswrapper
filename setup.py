#! /usr/bin/env python

import os

from setuptools import setup

packages = ['autoclasswrapper']

requires = [
    'chardet',
    'numpy',
    'pandas'
]

test_requirements = ['pytest>=2.8.0']

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'autoclasswrapper', '__version__.py'), 'r',
                       encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('HISTORY.md', 'r', encoding='utf-8') as f:
    history = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'autoclasswrapper': 'autoclasswrapper'},
    include_package_data=True,
    python_requires=">=3.4",
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD 3-Clause',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    )
)
