#!/bin/bash
source config/setting.conf
chmod +x *.py
rm -r $OUT_DIR
./scel_crawler.py --key=$KEYWORD --translate_omit=$TRANS_OMIT
./scel_parser.py
./rime_converter.py --target=$TARGET --dict=$DICT_PREFIX.$DICT_MASTER_NAME

[ -z $COPY ] || cp $OUT_DIR/* $COPY
[ -z '$HOOK_AFTER' ] || $HOOK_AFTER
echo 'Completed!'

