# -*- coding: utf-8 -*-
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import redis

from pythinkutils.common.StringUtils import *
from pythinkutils.common.log import g_logger

g_szSrcIP = "218.2.204.215"
g_nSrcPort = 6378
g_szSrcPassword = ""
g_nSrcDB = 2

def main():
    szHKey = "every_day_memintegral_2"
    rSrc = redis.Redis(host=g_szSrcIP, port=g_nSrcPort, password=g_szSrcPassword, db=g_nSrcDB)
    lstKeys = rSrc.hkeys(szHKey)

    nMaxPoint = 0
    for byteKey in lstKeys:
        szKey = byteKey.decode("utf-8")
        # g_logger.info(szKey)

        szRet = rSrc.hget("every_day_memintegral_2", szKey)
        szRet = szRet.decode("utf-8")

        if int(szRet) > nMaxPoint:
            nMaxPoint = int(szRet)

    g_logger.info(nMaxPoint)


if __name__ == '__main__':
    main()