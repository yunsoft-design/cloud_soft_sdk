#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 令牌生成及解密
创建    : 2022-05-29 8:23
更新    : 2022-05-29 8:23
编写    : 陈倚云
"""
from itsdangerous import URLSafeSerializer


class YsToken:
    """
    令牌生成及解密
    """

    def __init__(self, secret_key, salt):
        """
        令牌初始化,如果secret_key和salt均为空,则动态生成不可解的token,否则,生成可解密的token
        :param secret_key: 密钥
        :param salt: 盐
        """
        self._auth = URLSafeSerializer(secret_key, salt)

    def create_token(self, info):
        """
        生成token
        :param info: 加密信息
        :return:
        """

        token = self._auth.dumps(info)
        return token

    def decode_token(self, token):
        """
        获取token中的值
        :param token: 令牌
        :return:
        """
        info = self._auth.loads(token)
        return info
