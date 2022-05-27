#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : type.py
标题    : 类型
创建    : 2022-05-27 20:17
更新    : 2022-05-27 20:17
编写    : 陈倚云
"""
from enum import Enum, unique


@unique
class RequestType(Enum):
    """
    请求类型
    """
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'


class PayType(Enum):
    """
    支付类型
    """
    JSAPI = 0
    APP = 1
    H5 = 2
    NATIVE = 3
    MINIPROG = 4


class SignType(Enum):
    """
    加密解密类型
    """
    RSA_SHA256 = 0
    HMAC_SHA256 = 1
    MD5 = 2
