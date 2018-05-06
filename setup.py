#!/usr/bin/env python

from setuptools import setup, find_packages

PACKAGE = 'ddnz'
NAME = 'ddnz'
DESCRIPTION = 'let you know your ip address'
AUTHOR = 'zerosnake0'
AUTHOR_EMAIL = 'zerosnake0@gmail.com'
VERSION = __import__(PACKAGE).__version__

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      packages=find_packages(),
      install_requires=['dnspython', 'requests']
      )
