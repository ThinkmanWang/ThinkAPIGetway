# -*- coding: utf-8 -*-

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import requests
import json
import jwt
import redis

from pythinkutils.common.log import g_logger
from pythinkutils.config.Config import g_config
from pythinkutils.common.object2json import *
from pythinkutils.redis.ThinkRedis import ThinkRedis

g_dictAPIGetway = {
    "/": {
        "proxy_pass": "http://172.16.0.2:8001/"
    }
    , "/ruoyi-api/": {
        "proxy_pass": "http://172.16.0.2:8000/"
    }
    , "/prod-api/": {
        "proxy_pass": "http://172.16.0.2:8000/"
    }
}

def init_api_getway():
    r = redis.StrictRedis(connection_pool=ThinkRedis.get_conn_pool_ex())

    for szKey in g_dictAPIGetway.keys():
        r.hset("think_api_getway", szKey, json.dumps(g_dictAPIGetway[szKey]))

def main():
    g_logger.info("init api getway")
    init_api_getway()
    g_logger.info("Finish init api getway")

if __name__ == '__main__':
    main()