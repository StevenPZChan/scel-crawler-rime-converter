# scel-crawler-rime-converter
A 'sogou cell dictionary' crawler and a txt to RIME converter

### Requirement
* Python3
* Setup python3 bin directory into $PATH
* python package: re, requests

### Run
```shell
[ -d config ] || mkdir config
cp setting.conf.example config/setting.conf
vi config/setting.conf
chmod +x run.sh
./run.sh
```

All you need is to change some settings and run.
* KEYWORD -- scel crawler keyword
* TRANS_OMIT -- scel name translate to english
* OUT_DIR -- output directory for rime converter
* TARGET -- target code type
* DICT_PREFIX -- your rime input name
* DICT_MASTER_NAME -- your rime extension dict name, usually 'extended'
* COPY -- your rime config path
* HOOK_AFTER -- rime deploy script

### Scripts
* scel_crawler.py -- for scel crawler from sogou.com
* scel_parser.py -- parse word vocabulary from *.scel file
* rime_converter.py -- rime dict generator
##### You can just run some of them for partial requirement

