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
import random

from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
from urllib.parse import urlparse
from aiohttp_requests import requests
from io import BytesIO
import tornado.curl_httpclient
import tornado.httpclient
import tornado.httputil
import re

from pythinkutils.common.log import g_logger
from pythinkutils.aio.jwt.tornado.handler.BaseHandler import BaseHandler
from pythinkutils.aio.jwt.tornado.handler.JWTHandler import JWTHandler
from pythinkutils.common.StringUtils import *
from pythinkutils.common.object2json import obj2json
from pythinkutils.common.AjaxResult import AjaxResult

from enum import Enum
class APIGetwayResult(Enum):
    SUCCESS = 0
    UNKNOW_PATH = 1
    AUTH_INVALID = 2
    PROXY_FAILED = 3

class MainHandler(JWTHandler):

    g_dictAPIGetway = {}
    g_listAPIGetwayKey = []
    REDIS_KEY_API_GETWAY = "think_api_getway_v2"
    set_cookie_re = re.compile(";?\s*(domain|path)\s*=\s*[^,;]+", re.I)

    async def post(self, szPath):
        if False == str(szPath).startswith("/"):
            szPath = "/" + szPath.strip()

        nRet = await self.do_api_getway(szPath)

        if nRet == APIGetwayResult.SUCCESS:
            pass
        elif nRet == APIGetwayResult.UNKNOW_PATH:
            self.write(obj2json(AjaxResult.error("Unknow path '{}' ".format(szPath))))
        elif nRet == APIGetwayResult.AUTH_INVALID:
            self.write(obj2json(AjaxResult.error("Auth failed for '{}' ".format(szPath))))
        elif nRet == APIGetwayResult.PROXY_FAILED:
            self.write(obj2json(AjaxResult.error("Proxy failed for '{}' ".format(szPath))))
        else:
            self.write(obj2json(AjaxResult.error("Unknow Error for '{}' ".format(szPath))))


    async def get(self, szPath):
        await self.post(szPath)

    async def do_http_proxy_plus(self, szUrl):
        from pythinkutils.aio.common.aiolog import g_aio_logger

        try:
            # dictHeader = self.request.headers
            dictHeader = tornado.httputil.HTTPHeaders(self.request.headers)

            if "X-Forwarded-For" in dictHeader:
                dictHeader["X-Forwarded-For"] = "{}, {}".format(dictHeader.get("X-Forwarded-For", ""), self.get_client_ip())
            else:
                dictHeader["X-Forwarded-For"] = self.get_client_ip()

            url = urlparse(szUrl)
            # dictHeader["Host"] = url.netloc
            byteBody = self.request.body

            if "GET" == self.request.method or len(byteBody) <= 0:
                byteBody = None

            http_client = tornado.curl_httpclient.CurlAsyncHTTPClient()
            http_request = tornado.httpclient.HTTPRequest(
                szUrl
                , method=self.request.method
                , body=byteBody
                , headers=dictHeader
                , follow_redirects=True
                , allow_nonstandard_methods=True
                , decompress_response=False
                , request_timeout=60
            )

            response = await http_client.fetch(http_request)
            try:
                if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
                    self.set_status(500)
                    self.write('Internal server error:\n' + str(response.error))
                    await self.flush()

                    return APIGetwayResult.PROXY_FAILED
                else:
                    if response.headers.get('Transfer-Encoding') == 'chunked':
                        del response.headers['Transfer-Encoding']

                    if 'Set-Cookie' in response.headers:
                        set_cookie = response.headers.get_list('set-cookie')
                        del response.headers['set-cookie']

                        for each in set_cookie:
                            response.headers.add('set-cookie', self.set_cookie_re.sub('', each))
                    else:
                        pass

                    for szKey in response.headers.keys():
                        # if szKey == "Content-Length":
                        #     # Transfer-Encoding" and 'chunked
                        #     self.set_header("Transfer-Encoding", "chunked")
                        #     continue

                        szVal = response.headers.get(szKey)
                        self.set_header(szKey, szVal)

                    if response.body:
                        body = response.body
                        self.write(body)
                        await self.flush()

                    return APIGetwayResult.SUCCESS

            except Exception as e:
                self.set_status(500)
                self.write('Internal server error:\n')
                await self.flush()
                return APIGetwayResult.PROXY_FAILED
        except tornado.httpclient.HTTPClientError as e:
            if 304 == e.code:
                self.set_status(304)
                await self.flush()
                return APIGetwayResult.SUCCESS
        except Exception as e:
            return APIGetwayResult.PROXY_FAILED

    # async def do_http_proxy(self, szUrl):
    #     from pythinkutils.aio.common.aiolog import g_aio_logger
    #
    #     try:
    #
    #         # dictHeader = self.request.headers
    #         dictHeader = tornado.httputil.HTTPHeaders(self.request.headers)
    #         # dictHeader["Host"] = "{}://{}".format(url.scheme, url.netloc)
    #
    #         url = urlparse(szUrl)
    #         # dictHeader["Host"] = url.netloc
    #
    #         byteBody = self.request.body
    #
    #         if "POST" == self.request.method:
    #             if byteBody is None or 0 == len(byteBody):
    #                 resp = await requests.post(szUrl, headers=dictHeader)
    #             else:
    #                 resp = await requests.post(szUrl, headers=dictHeader, data=byteBody)
    #         else:
    #             resp = await requests.get(szUrl, headers=dictHeader)
    #
    #         # resp = await requests.request("POST", szUrl, headers=dictHeader, data=byteBody)
    #
    #         self.set_status(resp.status)
    #
    #         dictRespHeader = {}
    #
    #
    #         for k in dict(resp.headers).keys():
    #             if k == "Transfer-Encoding" and 'chunked' == resp.headers[k]:
    #                 continue
    #
    #             if k in dictRespHeader.keys():
    #                 dictRespHeader[k] = "{};{}".format(dictRespHeader[k], resp.headers[k])
    #             else:
    #                 dictRespHeader[k] = resp.headers[k]
    #
    #         for k in dictRespHeader.keys():
    #             self.add_header(k, dictRespHeader[k])
    #
    #         async for data in resp.content.iter_any():
    #             self.write(data)
    #             await self.flush()
    #
    #         return APIGetwayResult.SUCCESS
    #
    #     except Exception as e:
    #         return APIGetwayResult.PROXY_FAILED


    async def auth_valid(self, szKey):
        dictRule = MainHandler.g_dictAPIGetway[szKey]

        if "auth" not in dictRule.keys() or False == dictRule["auth"]:
            return True

        return await self.token_valid()

    def get_proxy_path(self, szKey):
        lstProxyPass = MainHandler.g_dictAPIGetway[szKey]["proxy_pass"]

        nSum = 0
        for dictItem in lstProxyPass:
            nSum += int(dictItem.get("weight", 1))

        nVal = random.randint(1, nSum)
        nSum = 0
        for dictItem in lstProxyPass:
            nSum += int(dictItem.get("weight", 1))
            if nVal <= nSum:
                return dictItem["host"]

        return lstProxyPass[0]["host"]


    async def do_api_getway(self, szPath):
        from pythinkutils.aio.common.aiolog import g_aio_logger

        try:
            for szKey in MainHandler.g_listAPIGetwayKey:
                if szPath.startswith(szKey):
                    # _szPath = szPath
                    szRealPath = "{}{}".format(self.get_proxy_path(szKey), szPath.replace(szKey, ""))
                    if "/" == szKey:
                        szRealPath = "{}{}".format(self.get_proxy_path(szKey), szPath[1:])

                    await g_aio_logger.info("Goto %s" % (szRealPath))

                    if False == await self.auth_valid(szKey):
                        return APIGetwayResult.AUTH_INVALID

                    return await self.do_http_proxy_plus(szRealPath)
                else:
                    continue

            return APIGetwayResult.UNKNOW_PATH
        except Exception as e:
            await g_aio_logger.error(e)
            return APIGetwayResult.PROXY_FAILED


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
