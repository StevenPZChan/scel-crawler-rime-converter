#!/bin/bash
source config/setting.conf
chmod +x *.py
./scel_crawler.py --key=$KEYWORD --translate_omit=$TRANS_OMIT
./scel_parser.py
./rime_converter.py --target=$TARGET --dict=$DICT_PREFIX.$DICT_MASTER_NAME
echo 'Completed!'

