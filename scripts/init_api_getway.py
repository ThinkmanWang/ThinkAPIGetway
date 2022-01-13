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
    "/think-ruoyi-api/": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://think-ruoyi-api:8087/"
                # , "weight": 1 #default 1
            }
            , {
                "host": "http://think-ruoyi-api:8087/"
                , "weight": 5 #default 1
            }
        ]
    }
    , "/ruoyi": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://think-ruoyi-ui/"
                , "weight": 1 #default 1
            }
        ]
    }
    , "/ruoyi/": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://think-ruoyi-ui/"
                , "weight": 1 #default 1
            }
        ]
    }
    , "/ws/game-ws-server": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "ws://game_main_server_01:8082/game"
                , "weight": 1 #default 1
            }
        ]
    }
    , "/yshop-api/": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://yshop-api:8000/"
                # , "weight": 1 #default 1
            }
        ]
    }
    , "/thinkspringboot/": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://thinkspringboot/"
                # , "weight": 1 #default 1
            }
        ]
    }

    , "/ruoyicound": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://ruoyicound-ui/"
                , "weight": 1 #default 1
            }
        ]
    }
    , "/ruoyicound/": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://ruoyicound-ui/"
                , "weight": 1 #default 1
            }
        ]
    }
    , "/ruoyicound-gateway/": {
        "auth": False
        , "proxy_pass": [
            {
                "host": "http://ruoyicound-gateway:8088/"
                # , "weight": 1 #default 1
            }
            , {
                "host": "http://ruoyicound-gateway:8088/"
                , "weight": 5 #default 1
            }
        ]
    }
    # , "/": {
    #     "auth": False
    #     , "proxy_pass": [
    #         {
    #             "host": "http://think-ruoyi-ui/"
    #             , "weight": 1 #default 1
    #         }
    #     ]
    # }
    # , "/ruoyi-api/": {
    #     "auth": False
    #     , "proxy_pass": [
    #         {
    #             "host": "http://172.16.0.2:8000/"
    #             # , "weight": 1 #default 1
    #         }
    #         , {
    #             "host": "http://172.16.0.2:8000/"
    #             , "weight": 5 #default 1
    #         }
    #     ]
    # }
    # , "/prod-api/": {
    #     "proxy_pass": [
    #         {
    #             "host": "http://172.16.0.2:8000/"
    #             , "weight": 1 #default 1
    #         }
    #     ]
    # }
    # , "/gogs/": {
    #     "proxy_pass": [
    #         {
    #             "host": "http://172.16.0.2:3000/"
    #             , "weight": 1 #default 1
    #         }
    #     ]
    # }
    # , "/gogs": {
    #     "proxy_pass": [
    #         {
    #             "host": "http://172.16.0.2:3000"
    #             , "weight": 1 #default 1
    #         }
    #     ]
    # }
}

def init_api_getway():
    r = redis.StrictRedis(connection_pool=ThinkRedis.get_conn_pool_ex())

    r.delete("think_api_getway_v2")

    for szKey in g_dictAPIGetway.keys():
        r.hset("think_api_getway_v2", szKey, json.dumps(g_dictAPIGetway[szKey]))

def main():
    g_logger.info("init api getway")
    init_api_getway()
    g_logger.info("Finish init api getway")

if __name__ == '__main__':
    main()