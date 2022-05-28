#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : exception.py
标题    : 自定义异常
创建    : 2022-05-27 10:58
更新    : 2022-05-27 10:58
编写    : 陈倚云
"""
class YsException(Exception):
    """
    自定义异常
    """

    def __init__(self, errcode='', direct='', errmsg='', errurl=''):
        self.errcode = errcode
        self.errmsg = str(errmsg)
        self.direct = direct
        self.errurl = errurl

    def __str__(self):
        error_info = {
            'errcode': self.errcode,  # 错误编码
            'errdir': self.direct,  # 错误路径
            'errmsg': self.errmsg,  # 错误提示
            'errurl': self.errurl  # 错误后跳转链接
        }
        return repr(error_info)
