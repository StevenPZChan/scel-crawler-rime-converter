#!/usr/bin/python3

import json
import requests
from threading import Thread

#translate_path = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i='
translate_path = 'http://fanyi.baidu.com/transapi?from=auto&to=en&query='

class TranslateHelper(Thread):
    trans_words = []
    def __init__(self, word, omit):
        super().__init__()
        self.word = word
        self.word_omit = word.replace(omit, '')

    def run(self):
        translate_json = json.loads(requests.get(translate_path + self.word_omit).text)

        try:
            #self.translate_word = translate_json['translateResult'][0][0]['tgt']
            self.translate_word = translate_json['data'][0]['dst']
        except Exception as e:
            print(e)
        else:
            self.trans_words.append((self.word, '_'.join(self.translate_word.lower().split())))

    def get_trans_word(self):
        return self.translate_word

