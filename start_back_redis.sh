#!/bin/sh

cd /root/Github-Thinkman/ThinkAPIGetway
export PATH="$PATH:/opt/bin"

pipenv run python scripts/backup_redis.py
