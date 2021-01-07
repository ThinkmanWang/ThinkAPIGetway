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
    REDIS_KEY_API_GETWAY = "think_api_getway"

    async def post(self, szPath):
        if False == str(szPath).startswith("/"):
            szPath = "/" + szPath.strip()

        self.write("{}".format(szPath))

    async def get(self, szPath):
        await self.post(szPath)

    @classmethod
    async def init_api_getway(cls):
        from pythinkutils.aio.common.aiolog import g_aio_logger
        from pythinkutils.aio.redis.ThinkAioRedisPool import ThinkAioRedisPool

        with await (await ThinkAioRedisPool.get_conn_pool_ex()) as conn:
            lstKey = await conn.execute('hkeys', cls.REDIS_KEY_API_GETWAY)

            for szKey in lstKey:
                # szKey = szKey.decode("utf8")
                szVal = await conn.execute('hget', cls.REDIS_KEY_API_GETWAY, szKey)

                if szVal is None:
                    continue

                cls.g_dictAPIGetway[szKey.decode("utf8")] = json.loads(szVal)

        await g_aio_logger.info(obj2json(cls.g_dictAPIGetway))
