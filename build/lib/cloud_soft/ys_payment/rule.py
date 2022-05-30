#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : rule.py
标题    : 加密解密规则
创建    : 2022-05-27 20:17
更新    : 2022-05-27 20:17
编写    : 陈倚云
"""
import json
import time
import uuid
from base64 import b64decode, b64encode

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate


def build_authorization(path,
                        method,
                        mchid,
                        serial_no,
                        private_key,
                        data=None,
                        nonce_str=None):
    """
    设置HTTP请求头: https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_0.shtml
    :param path:
    :param method:
    :param mchid:
    :param serial_no:
    :param private_key:
    :param data:
    :param nonce_str:
    :return:
    """
    time_stamp = str(int(time.time()))
    nonce_str = nonce_str or ''.join(str(uuid.uuid4()).split('-')).upper()
    body = data if isinstance(data, str) else json.dumps(data) if data else ''
    sign_str = '%s\n%s\n%s\n%s\n%s\n' % (method, path, time_stamp, nonce_str, body)
    signature = rsa_sign(private_key=private_key, sign_str=sign_str)
    authorization = 'WECHATPAY2-SHA256-RSA2048 mchid="%s",nonce_str="%s",ys_crypto="%s",timestamp="%s",serial_no="%s"' % (mchid, nonce_str, signature, time_stamp, serial_no)
    return authorization


def rsa_sign(private_key, sign_str):
    """
    计算签名值: https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_0.shtml
    :param private_key:
    :param sign_str:
    :return:
    """
    message = sign_str.encode('UTF-8')
    signature = private_key.sign(data=message, padding=PKCS1v15(), algorithm=SHA256())
    sign = b64encode(signature).decode('UTF-8').replace('\n', '')
    return sign


def aes_decrypt(nonce, ciphertext, associated_data, apiv3_key):
    """
    解密回调接口收到的信息:https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_2.shtml
    :param nonce:
    :param ciphertext:
    :param associated_data:
    :param apiv3_key:
    :return:
    """
    key_bytes = apiv3_key.encode('UTF-8')
    nonce_bytes = nonce.encode('UTF-8')
    associated_data_bytes = associated_data.encode('UTF-8')
    data = b64decode(ciphertext)
    aesgcm = AESGCM(key=key_bytes)
    try:
        result = aesgcm.decrypt(nonce=nonce_bytes, data=data, associated_data=associated_data_bytes).decode('UTF-8')
    except InvalidTag:
        result = None
    return result


def format_private_key(private_key_str):
    """
    格式化私钥
    :param private_key_str:
    :return:
    """
    pem_start = '-----BEGIN PRIVATE KEY-----\n'
    pem_end = '\n-----END PRIVATE KEY-----'
    if not private_key_str.startswith(pem_start):
        private_key_str = pem_start + private_key_str
    if not private_key_str.endswith(pem_end):
        private_key_str = str(private_key_str) + pem_end
    return private_key_str


def load_certificate(certificate_str):
    """
    加载证书
    :param certificate_str:
    :return:
    """
    try:
        return load_pem_x509_certificate(data=certificate_str.encode('UTF-8'), backend=default_backend())
    except:
        return None


def load_private_key(key_dir):
    """
    加载私钥
    :param key_dir:
    :return:
    """
    try:
        with open(key_dir) as f:
            private_key_str = f.read()
        return load_pem_private_key(data=format_private_key(private_key_str).encode('UTF-8'), password=None, backend=default_backend())
    except:
        raise Exception('failed to load private key.')


def rsa_verify(timestamp, nonce, body, signature, certificate):
    """
    公钥验证: https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_1.shtml
    :param timestamp:
    :param nonce:
    :param body:
    :param signature:
    :param certificate:
    :return:
    """
    sign_str = '%s\n%s\n%s\n' % (timestamp, nonce, body)
    public_key = certificate.public_key()
    message = sign_str.encode('UTF-8')
    signature = b64decode(signature)
    try:
        public_key.verify(signature, message, PKCS1v15(), SHA256())
    except InvalidSignature:
        return False
    return True
