#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is to parse word vocabulary from *.scel file.
:Author: StevenPZChan
:Reference: https://github.com/xwzhong/small-program/blob/master/scel-to-txt/scel2txt.py
"""
import os
import sys
from getopt import getopt

from Helper.ConfigHelper import ConfigHelper
from Utils.ScelParser import ScelParser

def usage():
    print('Usage: ./scel_parser.py [options]')
    print('Scel parser from *.scel to *.txt')
    print()
    print('  -h,\t--help\t\t\tHelp')
    print('  -i,\t--src=\t\t\tSet scel file directory')
    print('  -c,\t--config=\t\tSet config file')
    sys.exit(0)

if __name__ == '__main__':
    src_dir = 'download'
    config_file = None
    try:
        opts, args = getopt(sys.argv[1:], 'hi:c:', ['help', 'src=', 'config='])
        for option, value in opts:
            if option in ('-h', '--help'):
                usage()
            if option in ('-i', '--src'):
                src_dir = value
            if option in ('-c', '--config'):
                config_file = value
    except Exception as e:
        print('Wrong usage!')
        usage()

    config = ConfigHelper(config_file=config_file)
    config.read_config()
    parser_threads = []
    for scel, trans in config.words:
        parser_thread = ScelParser(os.path.join(src_dir, scel + '.scel'), trans)
        parser_threads.append(parser_thread)
        parser_thread.start()

    for thread in parser_threads:
        thread.join()
    print('Parse completed!')
    sys.exit(0)

