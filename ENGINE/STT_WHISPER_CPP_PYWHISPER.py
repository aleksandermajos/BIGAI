#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple Command Line Interface to test the package
"""
import argparse
import importlib.metadata
import logging

import pywhispercpp.constants as constants

__version__ = importlib.metadata.version('pywhispercpp')
print(__version__)