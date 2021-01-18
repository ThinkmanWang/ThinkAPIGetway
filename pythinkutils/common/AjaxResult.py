# -*- coding: utf-8 -*-

from pythinkutils.common.object2json import obj2json

class AjaxResult:
    def __init__(self, code=200, msg="success", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def error(cls, msg = None):
        if msg is None:
            return obj2json(AjaxResult(500, "Server Error"))
        else:
            return obj2json(AjaxResult(500, msg))

    @classmethod
    def success(cls, data):
        return obj2json(AjaxResult(data=data))