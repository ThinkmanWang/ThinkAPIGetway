#!/bin/sh

cd /root/Github-Thinkman/ThinkAPIGetway
export PATH="$PATH:/opt/bin"
export PATH="$PATH:/usr/local/bin"

pipenv run python scripts/backup_redis_plus.py -Dpname=backup_redis_plus > /dev/null 2>&1 &
