#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "tastyscrapy",
    version = "0.0.1",
    packages = find_packages('src'),
    package_dir = { '': 'src' },
    install_requires = [
        'setuptools',
        'scrapy >= 1.2.0, < 1.3.0',
    ],
)
