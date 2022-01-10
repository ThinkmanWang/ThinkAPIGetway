# -*- coding: utf-8 -*-

import asyncio
import jwt
from aiohttp_requests import requests

from pythinkutils.config.Config import g_config
from pythinkutils.common.object2json import *
from pythinkutils.aio.redis.ThinkAioRedisPool import ThinkAioRedisPool
from pythinkutils.aio.common.aiolog import g_aio_logger

class TokenUtils:

    g_szHost = g_config.get("auth", "host")
    JWT_SALT = ""

    @classmethod
    async def auth_token(cls, szAppId, szSecret):
        try:
            szUrl = "{}{}".format(TokenUtils.g_szHost, "/auth/token")
            resp = await requests.post(szUrl, data={"appid": szAppId, "secret": szSecret})

            if 200 != resp.status:
                return None

            dictRet = json.loads(await resp.text())
            if 200 != dictRet["code"]:
                return None

            return dictRet

        except Exception as ex:
            await g_aio_logger.error(ex)
            return None

    @classmethod
    async def get_info(cls, szToken):
        try:
            szUrl = "{}{}".format(TokenUtils.g_szHost, "/getInfo")
            dictHeader = {
                "Authorization": "Bearer {}".format(szToken)
            }

            resp = await requests.get(szUrl, headers=dictHeader)
            if 200 != resp.status:
                return None

            dictRet = json.loads(await resp.text())
            if 200 != dictRet["code"]:
                return None

            return dictRet

        except Exception as ex:
            await g_aio_logger.error(ex)
            return None

    @classmethod
    async def parse_token(cls, szToken):
        try:
            jwt_options = {
                'verify_signature': False,
                'verify_exp': True,
                'verify_nbf': False,
                'verify_iat': True,
                'verify_aud': False
            }

            dictToken = jwt.decode(szToken, TokenUtils.JWT_SALT, algorithms=["HS512"], options=jwt_options)
            return dictToken
        except Exception as ex:
            await g_aio_logger.error(ex)
            return None

    @classmethod
    async def expire_time(cls, szToken):
        try:
            dictToken = await cls.parse_token(szToken)
            if dictToken is None:
                return 0

            szKey = "login_tokens:{}".format(dictToken["login_user_key"])
            with await (await ThinkAioRedisPool.get_conn_pool_ex()) as conn:
                szVal = await conn.execute('ttl', szKey)
                return int(szVal)

        except Exception as ex:
            await g_aio_logger.error(ex)
            return 0

# async def main():
#     szToken = await TokenUtils.auth_token("1234", "5678")
#     await g_aio_logger.info(szToken)
#
#     dictRet = await TokenUtils.get_info(szToken)
#     await g_aio_logger.info(obj2json(dictRet))
#
#     await g_aio_logger.info(obj2json(await TokenUtils.parse_token(szToken)))
#     await g_aio_logger.info(await TokenUtils.expire_time(szToken))
#
#     # await g_aio_logger.shutdown()
#
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())