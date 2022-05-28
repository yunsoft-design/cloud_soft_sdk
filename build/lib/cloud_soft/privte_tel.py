#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : privte_tel.py
标题    : 华为隐私电话
创建    : 2022-05-27 18:08
更新    : 2022-05-27 18:08
编写    : 陈倚云
"""
import binascii
import datetime
import hashlib
import hmac
import json

import requests
import urllib3


class PrivateTel(object):
    """
    生成授权信息
    """

    def __init__(self, app_key, host, ak, sk):
        self.app_key = app_key
        self.host = host
        self.ak = ak
        self.sk = sk
        self._headers = {
            "AppKey": self.app_key,
            "X-Sdk-Date": self._get_utc_time(),
            "Content-Type": "application/json;charset=utf-8",
            "Host": self.host
        }

    def _signed_headers(self):
        """
        把header全部变成小写进行排序
        """
        a = []
        for key in self._headers:
            a.append(key.lower())
        a.sort()
        return a

    @staticmethod
    def _get_utc_time():
        """
        获取当前世界时间
        """
        return datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    def _canonical_headers(self):
        """
        把消息头转换为字符串
        """
        a = []
        headers = self._headers
        __headers = {}
        for key in headers:
            key_encoded = key.lower()
            value = headers[key]
            value_encoded = value.strip()
            __headers[key_encoded] = value_encoded
            headers[key] = value_encoded.encode("utf-8").decode('iso-8859-1')
        for key in self._signed_headers():
            a.append(key + ":" + __headers[key])
        return '\n'.join(a) + "\n"

    def _canonical_request(self, method, url, body):
        """
        拼接请求
        """
        canonical_headers = self._canonical_headers()
        sha256 = hashlib.sha256()
        sha256.update(body)
        hexencode = sha256.hexdigest()
        return "%s\n%s\n%s\n%s\n%s\n%s" % (method, url, '', canonical_headers, ";".join(self._signed_headers()), hexencode)

    @staticmethod
    def _hex_encode_sha256_hash(data):
        """
        hex加密
        :param data:
        :return:
        """
        sha256 = hashlib.sha256()
        sha256.update(data)
        return sha256.hexdigest()

    def _string_to_sign(self, canonical_request):
        """
        加密
        """
        auth_bytes = self._hex_encode_sha256_hash(canonical_request.encode('utf-8'))
        return "%s\n%s\n%s" % ("SDK-HMAC-SHA256", self._headers["X-Sdk-Date"], auth_bytes)

    def _hmacsha256(self, message):
        """
        不可逆键值对加密
        :param message:值
        :return:返回摘要,作为二进制数据字符串值
        """
        return hmac.new(self.sk.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    def _sign_string_to_sign(self, string_to_sign):
        """

        :param string_to_sign:
        :return:
        """
        hm = self._hmacsha256(string_to_sign)
        return binascii.hexlify(hm).decode()

    def _auth_header_value(self, signature, signed_headers):
        """
        加密
        :param signature:
        :param signed_headers:
        :return:
        """
        return "%s Access=%s, SignedHeaders=%s, Signature=%s" % (
            "SDK-HMAC-SHA256", self.ak, ";".join(signed_headers), signature)

    def _request_body(self, tel_a, tel_b, tel_x):
        """
        生成请求消息体
        :param tel_a:
        :param tel_b:
        :param tel_x:
        :return:
        """
        sub_time = self._get_utc_time()
        body = {
            "appKey": self.app_key,
            "requestId": "CMCCGX" + sub_time,
            "telXMode": "1",
            "telA": tel_a,
            "telB": tel_b,
            "telX": tel_x,
            "subTime": sub_time,
            "areaCode": "25",
            "expiration": "100",
            "remark": "huaweicall",
            "transId": "test_demo",
            "extra": {
                "callRecording": "1"
            }
        }
        return body

    def _header_generated(self, method, uri):
        """
        :param method:
        :param uri:
        :return:
        """

        signed_headers = self._signed_headers()  # 把header键全部变成小写进行排序
        canonical_request = self._canonical_request(method, uri, "".encode("utf-8"))
        string_to_sign = self._string_to_sign(canonical_request)
        signature = self._sign_string_to_sign(string_to_sign)
        authorization = self._auth_header_value(signature, signed_headers)
        self._headers["Authorization"] = authorization
        return self._headers

    def bind(self, tel_a, tel_b, tel_x):
        """
        :param tel_a:
        :param tel_b:
        :param tel_x:
        :return:
        """
        bind_uri = "/v1/ngin/axb/binding/"
        url = "http://" + self.host + bind_uri[:-1]
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #
        method = "POST"
        headers = self._header_generated(method, bind_uri)
        body = self._request_body(tel_a, tel_b, tel_x)
        # 当urllib3中禁用了请求警告时,如果设置了verify=False,则忽略https安全验证
        resp = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
        response = resp.json()
        if response.get('message', None) == 'Success':
            ret_info = {
                'message': 'Success',
                'tel_x': response['data']['telX'],
                'sub_id': response['data']['subId'],
            }
        else:
            ret_info = {
                'message': 'Failure'
            }
        return ret_info

    def unbind(self, tel_x, sub_id):
        """
        :param tel_x: 隐藏号
        :param sub_id: 绑定id
        """
        unbind_uri = "/v1/ngin/axb/binding/" + sub_id + '/' + tel_x + '/'
        url = "http://" + self.host + unbind_uri[:-1]
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #
        method = 'DELETE'
        headers = self._header_generated(method, unbind_uri)
        resp = requests.delete(url, headers=headers, verify=False)
        response = resp.json()
        return response.get('message', 'Failure')

    def get_voice_url(self, tel_x, sub_id):
        """
        :param tel_x: 中转
        :param sub_id: 绑定id
        :return:
        """
        voice_url = "/v1/ngin/axb/record/" + tel_x + '/' + sub_id + '/'
        url = "http://" + self.host + voice_url[:-1]
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #
        method = "GET"
        headers = self._header_generated(method, voice_url)
        resp = requests.get(url, headers=headers, verify=False)  # GET请求，用于获取录音文件地址
        response = resp.json()
        return response
