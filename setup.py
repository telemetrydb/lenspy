#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'lenspy'
DESCRIPTION = 'Plot big data with Python.'
AUTHOR = 'Seran Thirugnanam'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None
# What packages are required for this module to be executed?
REQUIRED = ["pandas",
            "plotly",
            "dash"]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(
        exclude=["demo", "tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
