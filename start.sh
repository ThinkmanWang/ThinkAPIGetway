#!/bin/sh

cd /root/Github-Thinkman/ThinkAPIGetway
export PATH="$PATH:/opt/bin"
export PATH="$PATH:/usr/local/bin"

pipenv run python scripts/init_api_getway.py
pipenv run python main.py -Dpname=ThinkAPIGetway > /dev/null 2>&1 &

