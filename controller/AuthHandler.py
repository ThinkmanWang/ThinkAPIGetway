# -*- coding: utf-8 -*-
import sys
import os

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

class AuthHandler(JWTHandler):

    async def post(self, szPath):
        if "token" == szPath:
            await self.auth()
        else:
            self.write(obj2json(AjaxResult.error("Unknow path {}".format(szPath))))

    async def get(self, szPath):
        await self.post(szPath)

    async def auth(self):
        dictToken = await self.create_token(self.get_argument("appid"), self.get_argument("secret"))

        if dictToken is None:
            return obj2json(AjaxResult.error())

        self.write(obj2json(dictToken))

