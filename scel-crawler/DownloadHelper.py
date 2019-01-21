#!/usr/bin/python3

import os
import requests
from threading import Thread

if not os.path.exists('download'):
    os.makedirs('download')

class DownloadHelper(Thread):
    def __init__(self, url, name):
        super().__init__()
        self.url = url
        self.name = name

    def run(self):
        scel_bin = requests.get(self.url).content
        file_name = 'download/' + self.name + '.scel'
        with open(file_name, 'wb') as f:
            f.write(scel_bin)
            print('Downloaded file:', self.name) 

