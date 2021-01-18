# -*- coding: utf-8 -*-

import sys
import os
import abc
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import user_agents

from pythinkutils.common.StringUtils import *
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *
from pythinkutils.common.AjaxResult import AjaxResult

class BaseHandler(tornado.web.RequestHandler):

    MAX_CLIENT_COUNT = 40960
    g_nClientCount = 0

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def get_user_agent(self):
        return self.request.headers.get("User-Agent", "")

    def max_client_reach(self):
        BaseHandler.g_nClientCount += 1
        return BaseHandler.g_nClientCount > BaseHandler.MAX_CLIENT_COUNT

    async def prepare(self):
        from pythinkutils.aio.common.aiolog import g_aio_logger

        if self.max_client_reach():
            self.write(AjaxResult.error("Too many requests"))
            await self.finish()
            return

        '''
        ua_string = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
        user_agent = parse(ua_string)
        
        # Accessing user agent's browser attributes
        user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
        user_agent.browser.family  # returns 'Mobile Safari'
        user_agent.browser.version  # returns (5, 1)
        user_agent.browser.version_string   # returns '5.1'
        
        # Accessing user agent's operating system properties
        user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
        user_agent.os.family  # returns 'iOS'
        user_agent.os.version  # returns (5, 1)
        user_agent.os.version_string  # returns '5.1'
        
        # Accessing user agent's device properties
        user_agent.device  # returns Device(family=u'iPhone', brand=u'Apple', model=u'iPhone')
        user_agent.device.family  # returns 'iPhone'
        user_agent.device.brand # returns 'Apple'
        user_agent.device.model # returns 'iPhone'
        
        # Viewing a pretty string version
        str(user_agent) # returns "iPhone / iOS 5.1 / Mobile Safari 5.1"
        '''
        try:
            szUA = await self.get_user_agent()

            user_agent = user_agents.parse(szUA)
            await g_aio_logger.info("%s %s %s" % (user_agent.device.family, user_agent.os.family, user_agent.browser.family ))
        except Exception as e:
            await g_aio_logger.error(e)

        await g_aio_logger.info("FROM %s %s %s" % (self.get_real_client_ip(), self.request.method, self.request.uri ))

    def on_finish(self):
        tornado.ioloop.IOLoop.current().add_callback(self.on_finish_async)

    async def on_finish_async(self):
        if BaseHandler.g_nClientCount > 0:
            BaseHandler.g_nClientCount -= 1

    def get_real_client_ip(self):
        try:
            szIP = self.request.headers.get("X-Forwarded-For")
            if szIP is None or len(szIP) <= 0 or "unknown" == szIP:
                szIP = self.request.headers.get("Proxy-Client-IP")

            if szIP is None or len(szIP) <= 0 or "unknown" == szIP:
                szIP = self.request.headers.get("WL-Proxy-Client-IP")

            if szIP is None or len(szIP) <= 0 or "unknown" == szIP:
                szIP = self.request.headers.get("X-Real-IP")

            if szIP is None or len(szIP) <= 0 or "unknown" == szIP:
                szIP = self.request.remote_ip

            if szIP is None or len(szIP) <= 0 or "unknown" == szIP:
                return ""

            return szIP.split(",")[0]

        except Exception as e:
            return self.request.remote_ip


    def get_client_ip(self):
        return self.request.remote_ip

    # async def get_uid(self):
    #     pass
    #
    # async def get_userinfo(self):
    #     pass
    #
    # async def get_token(self):
    #     pass
    #
    # async def get_permission_list(self):
    #     pass
