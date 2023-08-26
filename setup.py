#!/usr/bin/python3

## 
# @package setup.py 
# setup.py for distutils of ftpmounter
# Copyright 2019 linurs.org 
# Distributed under the terms of the GNU General Public License v2

from distutils.core import setup
setup(
      name="ftpmounter",
      scripts=["ftpmounter.py"],
      version="0.0",
      description='Mtp mounter',
      author='Urs Lindegger',
      author_email='urs@linurs.org',
      url='https://github.com/linurs/ftpmounter',
      download_url = "http://www.linurs.org/download/ftpmounter-0.0.tgz",
      keywords = ["mtp mount"],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
      ],
      long_description=open("README.md").read()     
)