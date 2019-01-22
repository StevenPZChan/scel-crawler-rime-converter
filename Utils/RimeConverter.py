#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
from threading import Thread

code_file = os.path.join('Utils', 'ChineseCode.txt')

class RimeConverter(Thread):
    out_dir = ''
    target = ''
    master_header = ''
    dict_prefix = ''
    dict_master_name = ''
    date = ''
    code_table = {}
    @classmethod
    def initial(cls, out_dir, target, dict_name):
        cls.out_dir = out_dir
        cls.target = target
        cls.dict_prefix, cls.dict_master_name = dict_name.split('.')
        if target == 'pinyin':
            imp = 'pinyin_simp'
        elif target in ('wubi', 'wubi86'):
            imp = 'wubi86'

        cls.date = datetime.date.today().strftime('%Y.%m.%d')
        cls.master_header = '\n'.join(('---',
            'name: ' + dict_name,
            'version: "' + cls.date + '"',
            'sort: by_weight',
            'use_preset_vocabulary: true',
            'import_tables:',
            '  - ' + imp,
            '',
        ))
        cls._load_code_table()
        os.path.exists(out_dir) or os.makedirs(out_dir)

    def __init__(self, src_dir, src_file):
        super().__init__()
        self.src_file = os.path.join(src_dir, src_file + '.txt')
        self.dict_name = self.dict_prefix + '.' + src_file
        out_file = '.'.join((self.dict_name, 'dict', 'yaml'))
        self.out_file = os.path.join(self.out_dir, out_file)
        self.header = '\n'.join(('---',
            'name: ' + self.dict_name,
            'version: "' + self.date + '"',
            'sort: by_weight',
            'use_preset_vocabulary: true',
            '...',
            '',
            '',
        ))

    def run(self):
        with open(self.src_file, 'r') as fi, open(self.out_file, 'w') as fo:
            fo.write(self.header)
            while True:
                line = fi.readline().strip()
                if not line:
                    break
                try:
                    word, py, count = line.split('\t')
                except Exception as e:
                    print(self.src_file)
                    print(line)
                    return

                if self.target == 'pinyin':
                    pass
                elif self.target in ('wubi', 'wubi86'):
                    py = self._wubi86_code(word)
                elif self.target == 'wubi98':
                    py = self._wubi98_code(word)
                else:
                    print(self.target + ': Code type not implemented!')
                    return

                fo.write('\t'.join((word, py, count)) + '\n')
        RimeConverter.master_header += '  - ' + self.dict_name + '\n'
        print('Converted file:', self.dict_name)

    @classmethod
    def write(cls):
        file_name = '.'.join((cls.dict_prefix, cls.dict_master_name, 'dict', 'yaml'))
        cls.master_header += '...\n\n'
        with open(os.path.join(cls.out_dir, file_name), 'w') as f:
            f.write(cls.master_header)

    @classmethod
    def _load_code_table(cls):
        with open(code_file, 'r') as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                neima, word, wubi86, wubi98, pinyin, count = line.split('\t')
                cls.code_table[word] = {
                    'neima': neima,
                    'wubi86': wubi86,
                    'wubi98': wubi98 or wubi86,
                    'pinyin': pinyin,
                }

    def __get_word_code(self, word, code):
        return self.code_table[word][code]

    def __get_wubi_code(self, word, code = 'wubi86'):
        word_len = len(word)
        if word_len == 1:
            return self.__get_word_code(word, code)

        codes = [self.__get_word_code(i, code) for i in word]
        if word_len == 2:
            return codes[0][:2] + codes[1][:2]
        elif word_len == 3:
            return codes[0][0] + codes[1][0] + codes[2][:2]
        else:
            return codes[0][0] + codes[1][0] + codes[2][0] + codes[-1][0]

    def _wubi86_code(self, word):
        return self.__get_wubi_code(word)

    def _wubi98_code(self, word):
        return self.__get_wubi_code(word, 'wubi98')

