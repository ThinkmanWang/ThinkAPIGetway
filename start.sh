#!/bin/sh

cd /root/Github-Thinkman/ThinkAPIGetway
export PATH="$PATH:/opt/bin"

pipenv run python main.py -Dpname=ThinkAPIGetway > /dev/null 2>&1 &
