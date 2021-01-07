# -*- coding: utf-8 -*-
import sys
import os
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
import aiomysql
from tornado.routing import RuleRouter, Rule, PathMatches

from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

from pythinkutils.common.log import g_logger
from pythinkutils.aio.jwt.tornado.handler.BaseHandler import BaseHandler
from pythinkutils.aio.jwt.tornado.handler.JWTHandler import JWTHandler
from pythinkutils.common.StringUtils import *
from pythinkutils.common.object2json import obj2json
from pythinkutils.common.AjaxResult import AjaxResult

class MainHandler(JWTHandler):

    g_dictAPIGetway = {}
    g_listAPIGetwayKey = []
    REDIS_KEY_API_GETWAY = "think_api_getway"

    async def post(self, szPath):
        if False == str(szPath).startswith("/"):
            szPath = "/" + szPath.strip()

        if await self.do_api_getway(szPath):
            pass
        else:
            # self.set_status(500)
            self.write(obj2json(AjaxResult.error("Unknow path '{}' ".format(szPath))))

    async def get(self, szPath):
        await self.post(szPath)

    async def do_api_getway(self, szPath):
        from pythinkutils.aio.common.aiolog import g_aio_logger

        for szKey in MainHandler.g_listAPIGetwayKey:
            if szPath.startswith(szKey):
                # _szPath = szPath
                szRealPath = "{}{}".format(MainHandler.g_dictAPIGetway[szKey]["proxy_pass"], szPath.replace(szKey, ""))
                if "/" == szKey:
                    szRealPath = "{}{}".format(MainHandler.g_dictAPIGetway[szKey]["proxy_pass"], szPath[1:])

                await g_aio_logger.info("Goto %s" % (szRealPath))

                return True

        return False


    @classmethod
    async def init_api_getway(cls):
        from pythinkutils.aio.common.aiolog import g_aio_logger
        from pythinkutils.aio.redis.ThinkAioRedisPool import ThinkAioRedisPool

        def key_cmp(szKey):
            return len(szKey)

        with await (await ThinkAioRedisPool.get_conn_pool_ex()) as conn:
            lstKey = await conn.execute('hkeys', cls.REDIS_KEY_API_GETWAY)

            for szKey in lstKey:
                szKey = szKey.decode("utf8")

                szVal = await conn.execute('hget', cls.REDIS_KEY_API_GETWAY, szKey)
                szVal = szVal.decode("utf8")

                if szVal is None:
                    continue

                cls.g_dictAPIGetway[szKey] = json.loads(szVal)

        await g_aio_logger.info(obj2json(cls.g_dictAPIGetway))

        for szKey in cls.g_dictAPIGetway.keys():
            cls.g_listAPIGetwayKey.append(szKey)

        cls.g_listAPIGetwayKey.sort(key=key_cmp, reverse=True)
