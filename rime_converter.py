#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is for rime dict generator.
:Author: StevenPZChan
"""
import sys
from getopt import getopt

from Helper.ConfigHelper import ConfigHelper
from Utils.RimeConverter import RimeConverter

def usage():
    print('Usage: ./rime_converter.py [options]')
    print('Rime dict generator from *.txt to *.dict.yaml packed')
    print()
    print('  -h,\t--help\t\t\tHelp')
    print('  -i,\t--src=\t\t\tSet txt file directory')
    print('  -o,\t--output=\t\tSet output file directory')
    print('  -c,\t--config=\t\tSet config file')
    print('  -t,\t--target=\t\tSet target code type')
    print('  -d,\t--dict=\t\t\tSet rime dict name')
    sys.exit(0)

if __name__ == '__main__':
    src_dir = 'parse'
    out_dir = 'rime'
    config_file = None
    target = 'pinyin'
    dict_name = 'luna_pinyin.extended'
    try:
        opts, args = getopt(sys.argv[1:], 'hi:o:c:t:d:', ['help', 'src=', 'output=', 'config=', 'target=', 'dict='])
        for option, value in opts:
            if option in ('-h', '--help'):
                usage()
            if option in ('-i', '--src'):
                src_dir = value
            if option in ('-o', '--output'):
                out_dir = value
            if option in ('-c', '--config'):
                config_file = value
            if option in ('-t', '--target'):
                target = value
            if option in ('-d', '--dict'):
                dict_name = value
    except Exception as e:
        print('Wrong usage!')
        usage()

    RimeConverter.initial(out_dir, target, dict_name)
    config = ConfigHelper(config_file=config_file)
    config.read_config()
    convert_threads = []
    for _, trans in config.words:
        convert_thread = RimeConverter(src_dir, trans)
        convert_threads.append(convert_thread)
        convert_thread.start()

    for thread in convert_threads:
        thread.join()
    RimeConverter.write()
    print('Convert completed!')
    sys.exit(0)

