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
from pythinkutils.common.StringUtils import *
from pythinkutils.common.object2json import obj2json
from pythinkutils.common.AjaxResult import AjaxResult

class IPHandler(BaseHandler):

    async def post(self):
        self.write(AjaxResult.success({"ip": self.get_real_client_ip()}))

    async def get(self):
        await self.post()
