#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from enum import Enum
from threading import Thread

# Multiple translate API
class TransApi(Enum):
    YOUDAO = 0
    BAIDU = 1
    GOOGLE = 2
    NUM_OF_API = 3

translate_path = {
    TransApi.YOUDAO: 'http://fanyi.youdao.com/translate?&doctype=json&type=ZH_CN2EN&i=',
    TransApi.BAIDU: 'http://fanyi.baidu.com/transapi?from=auto&to=en&query=',
    TransApi.GOOGLE: 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=en&q=',
}
result_path = {
    TransApi.YOUDAO: ('translateResult', 0, 0, 'tgt'),
    TransApi.BAIDU: ('data', 0, 'dst'),
    TransApi.GOOGLE: ('sentences', 0, 'trans'),
}

class TranslateHelper(Thread):
    trans_words = []
    trans_api = TransApi(0)
    def __init__(self, word, omit):
        super().__init__()
        self.word = word
        self.word_omit = word.replace(omit, '')

    def run(self):
        try:
            trans_url = translate_path[self.trans_api] + self.word_omit
            translate_json = json.loads(requests.get(trans_url).text)
            self.translate_word = self._get_result(translate_json, result_path[self.trans_api])
        except Exception as e:
            print(e)
            if self.trans_api.value < TransApi.NUM_OF_API.value:
                self.trans_api = TransApi(self.trans_api.value + 1)
                self.run()
            else:
                print('No usable translate API, please wait for some time.')
        else:
            trans_res = self.translate_word.encode('ascii', errors='ignore').decode('ascii').lower()
            self.trans_words.append((self.word, '_'.join(trans_res.split())))

    def get_trans_word(self):
        return self.translate_word

    def _get_result(self, ret, node):
        tmp = ret
        for n in node:
            tmp = tmp[n]
        return tmp

