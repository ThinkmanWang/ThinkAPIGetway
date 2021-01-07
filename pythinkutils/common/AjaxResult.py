# -*- coding: utf-8 -*-

class AjaxResult:
    def __init__(self, code=200, msg="", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def error(cls, data = None):
        return AjaxResult(500, "Server Error", data=data)

    @classmethod
    def success(cls, msg):
        return AjaxResult(msg=msg)