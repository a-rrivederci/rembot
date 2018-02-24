# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup (
    name='rembot',
    version='0.1.0',
    description='Rembot graphical user interface',
    long_description=README,
    url='http://github.com/attackle/rembot/',
    author='eeshiken',
    author_email='eeshiken@sfu.ca',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    zip_safe=False
)
