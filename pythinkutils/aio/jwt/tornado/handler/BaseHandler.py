# -*- coding: utf-8 -*-

import sys
import os
import abc
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pythinkutils.common.StringUtils import *
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def get_client_ip(self):
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
            return ""

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
