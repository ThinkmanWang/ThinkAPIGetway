# -*- coding: utf-8 -*-

import asyncio
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import websockets
import json

from asyncio_pool import AioPool
from aioredis import Redis
from tornado.websocket import websocket_connect

from controller.MainHandler import MainHandler
from pythinkutils.common.StringUtils import *

class WSHandler(tornado.websocket.WebSocketHandler):

    PREFIX = "/ws/"

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        self.m_corPool = None
        self.m_wsUpper = None
        self.m_bClosed = False

    def check_origin(self, origin):
        return True

    async def _get_real_url(self, szPath):
        from pythinkutils.aio.common.aiolog import g_aio_logger
        from pythinkutils.aio.redis.ThinkAioRedisPool import ThinkAioRedisPool

        r = Redis(connection_pool=await ThinkAioRedisPool.get_conn_pool_ex())
        try:
            szVal = await r.hget(MainHandler.REDIS_KEY_API_GETWAY, szPath.strip())
            szVal = szVal.decode("utf8")

            if is_empty_string(szVal):
                return None

            dictVal = json.loads(szVal)
            # if "proxy_pass" not in dictVal.keys():
            #     return None

            return dictVal["proxy_pass"][0]["host"]
        except Exception as ex:
            await g_aio_logger.error(ex)
            return None
        finally:
            await r.close()

    async def do_response(self):
        from pythinkutils.aio.common.aiolog import g_aio_logger
        while False == self.m_bClosed:
            try:
                szRet = await self.m_wsUpper.recv()
                if is_empty_string(szRet):
                    await g_aio_logger.info("FXXK")
                    continue

                await g_aio_logger.info("RESPONSE: %s" % (szRet, ))
                await self.write_message(szRet)
            except Exception as ex:
                self.close()


    async def open(self, szPath):
        from pythinkutils.aio.common.aiolog import g_aio_logger

        szPath = "{}{}".format(WSHandler.PREFIX, szPath)
        await g_aio_logger.info(szPath)

        # self.m_corPool = AioPool(size=1)
        szProxyUrl = await self._get_real_url(szPath)
        if is_empty_string(szProxyUrl):
            return

        self.m_wsUpper = await websockets.connect(szProxyUrl)
        asyncio.ensure_future(self.do_response())

    async def on_close(self):
        from pythinkutils.aio.common.aiolog import g_aio_logger
        self.m_bClosed = True

        try:
            await self.m_wsUpper.close()
        except Exception as ex:
            pass

        await g_aio_logger.info("Connection Closed")


    async def on_message(self, message):
        from pythinkutils.aio.common.aiolog import g_aio_logger

        await g_aio_logger.info(message)

        try:
            if self.m_wsUpper is None:
                return

            await self.m_wsUpper.send(message)
        except Exception as ex:
            await g_aio_logger.error(ex)
            self.close()
