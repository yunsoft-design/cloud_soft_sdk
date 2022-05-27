#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : applet.py
标题    : 小程序相关接口
创建    : 2022-05-27 10:39
更新    : 2022-05-27 10:39
编写    : 陈倚云
"""
import base64
import json
import requests
from Crypto.Cipher import AES
from django_redis import get_redis_connection
from .qr_code import QrCode
from .notice import Notice


class Applet(object):
    """
    小程序相关方法
    """

    def __init__(self, appid, app_secret, redis_alias,observer):
        self._appid = appid
        self._app_secret = app_secret
        self._redis_alias = redis_alias
        self._access_token = self.get_access_token()
        self._expire = 7000
        self.qrcode = QrCode(self._access_token,observer)
        self.nogice = Notice(self._access_token)

    def get_login_info(self, js_code):
        """
        :param js_code: 前端小程序登录时获取的登录信息
        :return: 包括会话密钥session_key在内的字典
        """
        wechat_url = 'https://api.weixin.qq.com/sns/jscode2session'
        param = {
            'appid': self._appid,
            'secret': self._app_secret,
            'js_code': js_code,
            'grant_type': 'authorization_code',
        }
        res = requests.get(url=wechat_url, params=param)
        res = json.loads(res.content)
        return res

    def get_access_token(self):
        """
        获取access_token
        """
        conn = get_redis_connection(self._redis_alias)
        access_token = conn.get(self._appid)  # 把appid做为保存access_token的关键字
        if access_token is None:
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/token'
            params = {
                'grant_type': 'client_credential',
                'appid': self._appid,
                'secret': self._app_secret
            }
            res = requests.get(url=wechat_url, params=params)
            res = json.loads(res.content)
            # 如果获取信息失败,多半是access_token错误,access_token错误的主要原因是白名单。要在微信公众平台首页白名单增加当前访问ip
            access_token = res['access_token']
            conn.set(self._appid, access_token, self._expire)
        else:
            access_token = bytes(access_token).decode()
        return access_token

    def decrypted_unionid(self, session_key, encrypted_data, iv):
        """
        :param session_key: 会话密钥
        :param encrypted_data: 加密字符串
        :param iv: 加密算法的初始向量
        :return: 用户信息
        """

        def _unpad(s):
            return s[:-ord(s[len(s) - 1:])]

        session_key = base64.b64decode(session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)
        cipher = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted = json.loads(_unpad(cipher.decrypt(encrypted_data)))
        if decrypted['watermark']['appid'] != self._appid:
            raise Exception('Invalid Buffer')
        return decrypted
