#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is to parse word vocabulary from *.scel file.
:Author: StevenPZChan
:Reference: https://github.com/xwzhong/small-program/blob/master/scel-to-txt/scel2txt.py
"""
import os
import sys

from Helper.ConfigHelper import ConfigHelper
from Utils import *

if __name__ == '__main__':
    os.path.exists('parse') or os.makedirs('parse')
    config = ConfigHelper()
    config.read_config()
    for scel, trans in config.words:
        ScelParser('download/' + scel + '.scel', 'parse/' + trans + '.txt').start()
    sys.exit(0)

