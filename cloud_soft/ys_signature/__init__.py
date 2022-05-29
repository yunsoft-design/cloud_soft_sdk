#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 签名
创建    : 2022-05-27 19:35
更新    : 2022-05-27 19:35
编写    : 陈倚云
"""

import base64
import json
import random
import string
import time
import uuid

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random


class YsSignature:
    """
    云软注册
    """

    @staticmethod
    def get_key(digit=32):
        """
        获取32位包含大小字字母数字在内的随机数,用于加密字符串
        :param digit:
        :return:
        """
        random_str = random.sample(string.ascii_letters + string.digits, digit)
        return ''.join(random_str)

    @staticmethod
    def get_app_number():
        """
        获取商户号
        :return:
        """
        return str(int(time.time() * 10000))

    @staticmethod
    def build_nonce_str():
        """
        获取32位随机字符串,也可做证书序列号
        :return:
        """
        return str(uuid.uuid4()).replace("-", "").upper()

    @staticmethod
    def get_private_pem():
        """
        生成私钥
        :return:
        """
        private_key = RSA.generate(1024, Random.new().read)
        private_pem = private_key.exportKey()
        return private_pem

    @staticmethod
    def get_public_key(private_pem):
        """
        根据私钥生成公钥
        :param private_pem:
        :return:
        """
        rsa = RSA.import_key(private_pem)
        public_pem = rsa.public_key().exportKey()
        return public_pem

    @staticmethod
    def encrypt(private_dir, clear_text):
        """
        公钥加密
        :param private_dir:私钥全路径名
        :param clear_text: 需要加密数据
        :return: 返回加密的数据
        """
        # 1 得到私钥
        with open(private_dir, 'rb') as f:
            private_pem = f.read()
        # 2 得到私钥
        private_key = RSA.import_key(private_pem)
        # 2 根据私钥公钥
        public_key = private_key.public_key()
        # 3 公钥加密
        cipher = PKCS1_v1_5.new(public_key)
        clear_text = str(clear_text).encode('utf-8')
        encrypted_msg = cipher.encrypt(clear_text)
        cipher_text = base64.b64encode(encrypted_msg)
        cipher_text = bytearray(cipher_text).decode('utf-8')
        return cipher_text

    @staticmethod
    def decrypt(private_dir, cipher_text):
        """
        私钥解密
        :param private_dir: 私钥名称
        :param cipher_text: 加密数据,即需解密的数据
        :return: 返回已解密的数据
        """
        with open(private_dir, 'rb') as f:
            private_pem = f.read()
        private_key = RSA.import_key(private_pem)
        cipher = PKCS1_v1_5.new(private_key)
        cipher_text = base64.b64decode(cipher_text)
        clear_text = cipher.decrypt(ciphertext=cipher_text, sentinel=private_key)
        clear_text = bytes(clear_text).decode('utf-8')
        try:
            clear_text = json.loads(clear_text)
            return clear_text
        except Exception:
            return clear_text
