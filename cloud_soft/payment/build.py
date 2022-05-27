#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : build.py
标题    : 交易模块
创建    : 2022-05-27 20:17
更新    : 2022-05-27 20:17
编写    : 陈倚云
"""
import json
import os
from datetime import datetime

import requests

from .type import RequestType
from .rule import (aes_decrypt, build_authorization, load_certificate, load_private_key, rsa_verify)


class Build:
    """
    生成请求
    """

    def __init__(self, mchid, cert_serial_no, key_dir, apiv3_key):
        self._mchid = mchid
        self._cert_serial_no = cert_serial_no

        self._private_key = load_private_key(key_dir)
        self._apiv3_key = apiv3_key
        self._gate_way = 'https://api.mch.weixin.qq.com'
        self._certificates = []
        self._cert_dir = self.get_cert_dir(key_dir)

    @staticmethod
    def get_cert_dir(key_dir):
        """
        获取证书路径
        :param key_dir:
        :return:
        """
        cert_dir, filename = os.path.split(key_dir)
        return cert_dir + '/'

    def _update_certificates(self):
        path = '/v3/certificates'
        self._certificates.clear()
        code, message = self.request(path, skip_verify=True)
        if code != 200:
            return
        data = json.loads(message).get('data')
        for value in data:
            serial_no = value.get('serial_no')
            effective_time = value.get('effective_time')
            expire_time = value.get('expire_time')
            encrypt_certificate = value.get('encrypt_certificate')
            algorithm = nonce = associated_data = ciphertext = None
            if encrypt_certificate:
                algorithm = encrypt_certificate.get('algorithm')
                nonce = encrypt_certificate.get('nonce')
                associated_data = encrypt_certificate.get('associated_data')
                ciphertext = encrypt_certificate.get('ciphertext')
            if not (serial_no and effective_time and expire_time and algorithm and nonce and associated_data and ciphertext):
                continue
            cert_str = aes_decrypt(
                nonce=nonce,
                ciphertext=ciphertext,
                associated_data=associated_data,
                apiv3_key=self._apiv3_key)
            certificate = load_certificate(cert_str)
            if not certificate:
                continue
            now = datetime.utcnow()
            if now < certificate.not_valid_before or now > certificate.not_valid_after:
                continue
            self._certificates.append(certificate)
            if not self._cert_dir:
                continue
            if not os.path.exists(self._cert_dir):
                os.makedirs(self._cert_dir)
            if not os.path.exists(self._cert_dir + serial_no + '.pem'):
                f = open(self._cert_dir + serial_no + '.pem', 'w')
                f.write(cert_str)
                f.close()

    def _verify_signature(self, headers, body):
        signature = headers.get('Wechatpay-Signature')
        timestamp = headers.get('Wechatpay-Timestamp')
        nonce = headers.get('Wechatpay-Nonce')
        serial_no = headers.get('Wechatpay-Serial')
        cert_found = False
        certificate = False
        for cert in self._certificates:
            if int('0x' + serial_no, 16) == cert.serial_number:
                cert_found = True
                certificate = cert
                break
        if not cert_found:
            self._update_certificates()
            for cert in self._certificates:
                if int('0x' + serial_no, 16) == cert.serial_number:
                    cert_found = True
                    certificate = cert
                    break
            if not cert_found:
                return False
        if not rsa_verify(timestamp, nonce, body, signature, certificate):
            return False
        return True

    def request(self, path, method=RequestType.GET, data=None, skip_verify=False):
        """
        生成请求
        :param path:微信支付请求路径,去掉'https://api.mch.weixin.qq.com'公共路径后剩余的路径
        :param method:微信支付请求方式
        :param data:拼接的请求体
        :param skip_verify:
        :return:
        """
        authorization = build_authorization(
            path,
            method.value,
            self._mchid,
            self._cert_serial_no,
            self._private_key,
            data=data)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'yunsoft payment sdk(https://www.csoft.com)',
            # 'Wechatpay-Serial': hex(self._last_certificate().serial_number)[2:].upper(),
            'Authorization': authorization

        }
        if method == RequestType.GET:
            response = requests.get(url=self._gate_way + path, headers=headers)
        elif method == RequestType.POST:
            response = requests.post(url=self._gate_way + path, json=data, headers=headers)
        elif method == RequestType.PATCH:
            response = requests.patch(url=self._gate_way + path, json=data, headers=headers)
        elif method == RequestType.PUT:
            response = requests.put(url=self._gate_way + path, json=data, headers=headers)
        elif method == RequestType.DELETE:
            response = requests.delete(url=self._gate_way + path, headers=headers)
        else:
            raise Exception('微信不支持的请求方式.')
        if response.status_code in range(200, 300) and not skip_verify:
            if not self._verify_signature(response.headers, response.text):
                raise Exception('签名验证失败')
        return response.status_code, response.text if 'application/json' in response.headers.get('Content-Type') else response.content

    def decrypt_callback(self, headers, body):
        """
        解密回调接口收到的信息
        :param headers:
        :param body:
        :return:
        """
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
        if not self._verify_signature(headers, body):
            return None
        data = json.loads(body)
        resource_type = data.get('resource_type')
        if resource_type != 'encrypt-resource':
            return None
        resource = data.get('resource')
        if not resource:
            return None
        algorithm = resource.get('algorithm')
        if algorithm != 'AEAD_AES_256_GCM':
            raise Exception('sdk does not support this algorithm')
        nonce = resource.get('nonce')
        ciphertext = resource.get('ciphertext')
        associated_data = resource.get('associated_data')
        if not (nonce and ciphertext):
            return None
        if not associated_data:
            associated_data = ''
        result = aes_decrypt(
            nonce=nonce,
            ciphertext=ciphertext,
            associated_data=associated_data,
            apiv3_key=self._apiv3_key)
        return result

    def callback(self, headers, body):
        """
        回调接口
        :param headers:
        :param body:
        :return:
        """
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
        result = self.decrypt_callback(headers=headers, body=body)
        if result:
            data = json.loads(body)
            data.update({'resource': json.loads(result)})
            return data
        else:
            return result

    def _last_certificate(self):
        if not self._certificates:
            self._update_certificates()
        certificate = self._certificates[0]
        for cert in self._certificates:
            if certificate.not_valid_after < cert.not_valid_after:
                certificate = cert
        return certificate
