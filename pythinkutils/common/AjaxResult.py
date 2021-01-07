# -*- coding: utf-8 -*-

class AjaxResult:
    def __init__(self, code=200, msg="", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def error(cls, msg = None):
        if msg is None:
            return AjaxResult(500, "Server Error")
        else:
            return AjaxResult(500, msg)

    @classmethod
    def success(cls, data):
        return AjaxResult(data=data)