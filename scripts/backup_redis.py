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
g_nSrcDB = 0

g_szDestIP = "127.0.0.1"
g_nDestPort = 6379
g_szDestPassword = "Ab123145"
g_nDestDB = 4

def main():
    global g_szSrcIP
    global g_nSrcPort
    global g_szSrcPassword
    global g_nSrcDB

    global g_szDestIP
    global g_nDestPort
    global g_szDestPassword
    global g_nDestDB

    try:
        if is_empty_string(g_szSrcPassword):
            g_szSrcPassword = None

        if is_empty_string(g_szDestPassword):
            g_szDestPassword = None

        if g_nSrcDB < 0:
            g_nSrcDB = 0

        if g_nDestDB < 0:
            g_nDestDB = 0

        rSrc = redis.Redis(host=g_szSrcIP, port=g_nSrcPort, password=g_szSrcPassword, db=g_nSrcDB)
        rDest = redis.Redis(host=g_szDestIP, port=g_nDestPort, password=g_szDestPassword, db=g_nDestDB)

        lstKeys = rSrc.keys()
        if lstKeys is None or len(lstKeys) <= 0:
            return

        nPos = 0
        nSuccess = 0
        for byteKey in lstKeys:
            nPos += 1
            szKey = byteKey.decode("utf-8")

            byteVal = rSrc.dump(szKey)
            if byteVal is None:
                g_logger.info("Value for %s is null" % (szKey, ))
                continue

            nTTL = rSrc.ttl(szKey)
            if nTTL < 0:
                nTTL = 0

            byteRet = rDest.restore(szKey, nTTL, byteVal, replace=True)
            szRet = byteRet.decode("utf-8")

            if "OK" == szRet:
                nSuccess += 1
            else:
                g_logger.error("RESTORE KEY %s FAILED (%s)" % (szKey, szRet))
                return

            g_logger.info("%d/%d [SUCCESS: %d] => %s" % (nPos, len(lstKeys), nSuccess, szKey))
            
        g_logger.info("FINISHED: %d/%d [SUCCESS: %d]" % (nPos, len(lstKeys), nSuccess))
    except Exception as ex:
        g_logger.error(ex)
        return

if __name__ == '__main__':
    main()