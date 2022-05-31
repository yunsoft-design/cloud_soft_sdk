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
import ast

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PkcsCipher
from Crypto.Signature import PKCS1_v1_5 as PkcsSignature
from Crypto.Hash import SHA256
from Crypto import Random


class YsCrypto:
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
        cipher = PkcsCipher.new(public_key)
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
        cipher = PkcsCipher.new(private_key)
        cipher_text = base64.b64decode(cipher_text)
        clear_text = cipher.decrypt(ciphertext=cipher_text, sentinel=private_key)
        clear_text = bytes(clear_text).decode('utf-8')
        try:
            clear_text = ast.literal_eval(clear_text)
            return clear_text
        except Exception:
            return clear_text

    @staticmethod
    def rsa_sign(private_dir, sign_str):
        """
        私钥签名
        :param private_dir:
        :param sign_str:
        :return:
        """
        with open(private_dir, 'rb') as f:
            private_pem = f.read()
        private_key = RSA.import_key(private_pem)
        signer = PkcsSignature.new(private_key)
        rand_hash = SHA256.new()
        rand_hash.update(json.dumps(sign_str).encode('utf-8'))
        signature = signer.sign(rand_hash)
        return signature

    @staticmethod
    def get_sign_str(method, path, time_stamp, nonce_str, body):
        """
        生成加密字符串
        :param method:
        :param path:
        :param time_stamp:
        :param nonce_str:
        :param body:
        :return:
        """
        sign_str = '%s\n%s\n%s\n%s\n%s\n' % (method, path, time_stamp, nonce_str, body)
        return sign_str

    @staticmethod
    def build_authorization(path,
                            method,
                            user_info_id,
                            serial_no,
                            private_dir,
                            data=None
                            ):
        """
        生成授权
        :param path:
        :param method:
        :param user_info_id:
        :param serial_no:
        :param private_dir:
        :param data:
        :return:
        """
        time_stamp = str(int(time.time()))
        nonce_str = ''.join(str(uuid.uuid4()).split('-')).upper()
        body = data if isinstance(data, str) else json.dumps(data) if data else ''
        sign_str = YsCrypto.get_sign_str(method, path, time_stamp, nonce_str, body)
        signature = YsCrypto.rsa_sign(private_dir=private_dir, sign_str=sign_str)
        authorization = 'Cloud-Soft-SHA256 user_info_id=%s,nonce_str=%s,timestamp=%s,serial_no=%s,signature=%s' % (user_info_id, nonce_str, time_stamp, serial_no, signature)
        return authorization

    @staticmethod
    def verify_sign(signature, sign_str, private_dir):
        """
        验签
        :param signature:
        :param sign_str:
        :param private_dir:
        :return:
        """
        # 1 得到私钥
        with open(private_dir, 'rb') as f:
            private_pem = f.read()
        # 2 得到私钥
        private_key = RSA.import_key(private_pem)
        # 2 根据私钥公钥
        public_key = private_key.public_key()
        verifier = PkcsSignature.new(public_key)
        _rand_hash = SHA256.new()
        _rand_hash.update(json.dumps(sign_str).encode('utf-8'))
        signature = bytes(signature)
        verify = verifier.verify(_rand_hash, signature)
        return verify
