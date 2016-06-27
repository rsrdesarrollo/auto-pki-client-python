#!/usr/bin/env python
"""
EST Client
==========
"""
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "auto-pki-client",
    version = "0.1",
    author = "Raúl Sampedro",
    author_email = "rsrdesarrollo@gmail.com",
    description = ('Client to interact with an EST server - RFC 7030.'),
    license = "GPL-3.0",
    keywords = "Enrollment secure transport",
    packages=['est'],
    install_requires=[
        'pyYaml',
        'zeroconf'
    ],
    dependency_link=[
        'https://github.com/rsrdesarrollo/est-client-python/tarball/master#egg=est'
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
