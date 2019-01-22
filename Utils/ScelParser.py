#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import struct
from threading import Thread

os.path.exists('parse') or os.makedirs('parse')

class ScelParser(Thread):
    _start_pinyin = 0x1540  # pinyin offset
    _start_vocab = 0x2628   # vocabulary offset
    _scel_token = b'\x40\x15\x00\x00\x44\x43\x53\x01\x01\x00\x00\x00'   # scel start token
    _pinyin_token = b'\x9D\x01\x00\x00' # pinyin table start token
    def __init__(self, scel_name, file_name):
        super().__init__()
        self.scel_name = scel_name
        self.file_name = re.sub(r'[?*/\<>:"|]', '', file_name) + '.txt'
        self.pinyin_table = {}
        self.result = []

    def run(self):
        with open(self.scel_name, 'rb') as f:
            data = f.read()
        if data[:12] != self._scel_token:
            print(self.scel_name, 'is not .scel vocabulary!')
            return

        self._get_pinyin_table(data[self._start_pinyin:self._start_vocab])
        self._get_vocab(data[self._start_vocab:])
        self._write()

    def _int_parse(self, data):
        if len(data) != 2:
            return None
        return struct.unpack('H', data)[0]

    def _byte2str(self, data):
        length = len(data)
        ret = [chr(self._int_parse(data[i:i + 2])) for i in range(0, length, 2)]
        return ''.join(ret).replace(' ', '').replace('\r', '\n')

    def _get_pinyin_table(self, data):
        if len(data) < 4 or data[:4] != self._pinyin_token:
            return None

        pos = 4
        length = len(data)
        while pos < length:
            index = self._int_parse(data[pos:pos + 2])
            pos += 2
            l = self._int_parse(data[pos:pos + 2])
            pos += 2
            py = self._byte2str(data[pos:pos + l])
            self.pinyin_table[index] = py
            pos += l

    def _get_word_pinyin(self, data):
        length = len(data)
        ret = [self.pinyin_table[self._int_parse(data[i:i + 2])] for i in range(0, length, 2)]
        return ' '.join(ret)

    def _get_vocab(self, data):
        pos = 0
        length = len(data)
        while pos < length:
            same = self._int_parse(data[pos:pos + 2])
            pos += 2
            py_table_len = self._int_parse(data[pos:pos + 2])
            pos += 2
            try:
                py = self._get_word_pinyin(data[pos:pos + py_table_len])
            except KeyError:
                continue
            finally:
                pos += py_table_len

            for i in range(same):
                try:
                    c_len = self._int_parse(data[pos:pos + 2])
                except struct.error:
                    continue
                finally:
                    pos += 2

                try:
                    word = self._byte2str(data[pos:pos + c_len])
                except struct.error:
                    continue
                finally:
                    pos += c_len

                ext_len = self._int_parse(data[pos:pos + 2])
                pos += 2
                count = self._int_parse(data[pos:pos + 2])
                self.result.append((word, py, count))
                pos += ext_len

    def _write(self):
        file_name = os.path.join('parse', self.file_name)
        with open(file_name, 'w') as f:
            for word, py, count in self.result:
                f.write(str(word) + '\t' + py + '\t' + str(count) + '\n')
            print('Parsed file:', self.file_name)

