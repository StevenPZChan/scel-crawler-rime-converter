#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from threading import Thread

os.path.exists('download') or os.makedirs('download')

class DownloadHelper(Thread):
    def __init__(self, url, name):
        super().__init__()
        self.url = url
        self.name = name + '.scel'

    def run(self):
        scel_bin = requests.get(self.url).content
        file_name = os.path.join('download', self.name)
        with open(file_name, 'wb') as f:
            f.write(scel_bin)
            print('Downloaded file:', self.name)

