# -*- coding: utf-8 -*-
import sys
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import aiocron

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
from controller.MainHandler import MainHandler
from controller.AuthHandler import AuthHandler

# @aiocron.crontab("*/1 * * * *")
async def sync_apigetway():
    await MainHandler.init_api_getway()

async def on_server_started():
    g_logger.info("Server Started!!!")
    tornado.httpclient.AsyncHTTPClient.configure(None, max_clients=10240)
    # tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

    await MainHandler.init_api_getway()

    #crontab
    aiocron.crontab("*/1 * * * *", func=sync_apigetway)


application = tornado.web.Application(handlers = [
    (r"/auth/(.*)", AuthHandler)
    , (r"/(.*)", MainHandler)
], cookie_secret="BUEa2ckrQtmBofim3aP6cwr/acg0LEu6mHUxq4O3EY0=", autoreload=False)

if __name__ == '__main__':

    http_server = HTTPServer(application)

    http_server.bind(80)
    http_server.start(0)
    # http_server.listen(8080)

    g_logger.info('HTTP Server started... %d' % (os.getpid(),))
    asyncio.gather(on_server_started())

    tornado.ioloop.IOLoop.current().start()
