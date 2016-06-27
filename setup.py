#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auto PKI Client
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
    name = "auto_pki_client",
    version = "0.1.1",
    author = "Raúl Sampedro",
    author_email = "rsrdesarrollo@gmail.com",
    description = ('Client to interact with an EST server - RFC 7030.'),
    license = "GPL-3.0",
    keywords = "Enrollment secure transport",
    scripts=['scripts/auto-pki-client'],
    packages=[
        'auto_pki_client',
        'auto_pki_client.aux',
        'auto_pki_client.configuration',
    ],
    install_requires=[
        'pyYaml',
        'zeroconf',
        'est>=0.2.1'
    ],
    dependency_links=[
        'https://github.com/rsrdesarrollo/est-client-python/tarball/master#egg=est-0.2.1'
    ],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
        'Programming Language :: Python'
    ],
)
