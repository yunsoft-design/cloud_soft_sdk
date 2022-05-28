#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : sms.py
标题    : 
创建    : 2022-05-27 17:39
更新    : 2022-05-27 17:39
编写    : 陈倚云
"""
import json
import time
import uuid
import hashlib
import base64
import requests  # 需要先使用pip install requests命令安装依赖
import random
import re
from django_redis import get_redis_connection


class YsSms:
    """
    华为短信发送
    """

    def __init__(self, url, appkey,app_secret,sender, template_id, redis_alias):
        self._url = url # APP接入地址(在控制台"应用管理"页面获取)+接口访问URI
        self._APP_KEY = appkey  # APP_Key
        self._APP_SECRET = app_secret
        self._sender = sender # 国内短信签名通道号或国际/港澳台短信通道号
        self._template_id = template_id
        self._redis_alias = redis_alias

    def build_wsse_header(self):
        """
        生成WSSE
        """
        now = time.strftime('%Y-%m-%dT%H:%M:%SZ')  # Created
        nonce = str(uuid.uuid4()).replace('-', '')  # Nonce
        digest = hashlib.sha256((nonce + now + self._APP_SECRET).encode()).hexdigest()
        digest_base64 = base64.b64encode(digest.encode()).decode()  # PasswordDigest
        return 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}"'.format(self._APP_KEY, digest_base64, nonce, now)

    def get_header(self):
        """
        获取请求头
        """
        header = {'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
                  'X-WSSE': self.build_wsse_header()}
        return header

    @staticmethod
    def get_code():
        """
        生成6位验证码
        """
        code = ''
        for x in range(0, 6):
            code += str(random.randint(0, 9))
        return code

    def send(self, receiver):
        """
        发送消息
        """
        conn = get_redis_connection(self._redis_alias)
        ret = conn.get(receiver)
        status = 200
        if ret is None:
            header = self.get_header()
            code = self.get_code()
            data = {
                'from': self._sender,
                'to': receiver,
                'templateId': self._template_id,
                'templateParas': '["' + code + '"]',
                'statusCallback': "",
            }
            res = requests.post(self._url, data=data, headers=header, verify=False)
            content = json.loads(res.content)
            if content['description'] == 'Success':
                conn.set(receiver, code)
                conn.expire(receiver, 60 * 60 * 24 * 365)
            else:
                status = 400
        return {
            'status': status
        }

    @staticmethod
    def mobile_is_valid(phone_str):
        """
        验证手机号是否合法
        """
        if re.match(r'1[3,4,5,7,8]\d{9}', phone_str):
            return True
        else:
            return False

    def verify_sms(self, receiver, sms_code):
        """
        验证验证码
        """
        conn = get_redis_connection(self._redis_alias)
        ret = conn.get(receiver)
        result = False
        if ret is not None:
            code = str(bytes(ret).decode('utf-8'))
            if code == sms_code:
                result = True
        return {
            'result': result
        }
