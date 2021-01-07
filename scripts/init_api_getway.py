# -*- coding: utf-8 -*-

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
}

def init_api_getway():
    r = redis.StrictRedis(connection_pool=ThinkRedis.get_conn_pool_ex())

    for szKey in g_dictAPIGetway.keys():
        r.hset("think_api_getway", szKey, json.dumps(g_dictAPIGetway[szKey]))

def main():
    init_api_getway()

if __name__ == '__main__':
    main()