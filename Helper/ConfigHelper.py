#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

os.path.exists('config') or os.makedirs('config')

class ConfigHelper:
    def __init__(self, words = []):
        self.words = words
        self.config_file = 'config/trans.conf'

    def write_config(self):
        with open(self.config_file, 'w') as f:
            for w, t in self.words:
                f.write(w + '\t' + t + '\n')

    def read_config(self):
        with open(self.config_file, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                self.words.append(line.split())

