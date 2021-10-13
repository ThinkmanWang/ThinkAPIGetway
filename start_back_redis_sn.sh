#!/bin/sh

cd /root/Github-Thinkman/ThinkAPIGetway
export PATH="$PATH:/opt/bin"
export PATH="$PATH:/usr/local/bin"
export PATH="$PATH:/usr/bin"

pipenv run python scripts/backup_redis_plus_sn.py -Dpname=backup_redis_plus_sn > /dev/null 2>&1 &
