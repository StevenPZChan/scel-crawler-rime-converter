#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This python script is for scel crawler from sogou.com.
:Author: StevenPZChan
"""
import re
import requests
import sys
from getopt import getopt
from lxml import etree

from Helper import *

def usage():
    print('Usage: ./scel_crawler.py [options]')
    print('Scel crawler from sogou.com')
    print()
    print('  -h,\t--help\t\t\tHelp')
    print('  \t--key=\t\t\tSet search key word')
    print('  \t--translate_omit=\tSet translate omit word')
    sys.exit(0)

if __name__ == '__main__':
    key_word = None
    translate_omit = ''
    try:
        opts, args = getopt(sys.argv[1:], 'h', ['help', 'key=', 'translate_omit='])
        for option, value in opts:
            if option in ('-h', '--help'):
                usage()
            if option == '--key':
                key_word = value
            if option == '--translate_omit':
                translate_omit = value
    except Exception as e:
        print('No specified keyword! Using keyword: 【官方推荐】')

    key_word = key_word or '【官方推荐】'
    search_results = 'http://wubi.sogou.com/dict/search.php?word=' + \
        requests.utils.quote(key_word, encoding='gbk') + \
        '&searchOption=dict&type=0&personal=1&page='
    scel_download_path = ['http://download.pinyin.sogou.com/dict/download_cell.php?id=', '&name=']
    id_xpath = ['//*[@id="searchres"]/div[', ']/h2/a']
    translate_threads = []

    i = 1  # Start from page 1
    while True:
        search_page = search_results + str(i)
        page_info = requests.get(search_page).content
        html = etree.HTML(page_info)
        has_result = False
        for j in range(10):
            result = html.xpath(id_xpath[0] + str(j + 1) + id_xpath[1])
            if not result:
                continue

            scel_url = result[0].get('href')
            num = re.findall(r'id=(\d+)', scel_url)
            if not num:
                continue

            has_result = True
            scel_num = num[0]
            scel_name = result[0].text
            scel_download = scel_download_path[0] + scel_num + scel_download_path[1] + scel_name
            scel_name = scel_name.replace('/', '_')
            DownloadHelper(scel_download, scel_name).start()
            translate_thread = TranslateHelper(scel_name, translate_omit)
            translate_threads.append(translate_thread)
            translate_thread.start()

        i += 1
        if not has_result:
            break

    for thread in translate_threads:
        thread.join()

    ConfigHelper(TranslateHelper.trans_words).write_config()
    sys.exit(0)

