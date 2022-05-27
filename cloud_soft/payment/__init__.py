#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 云软微信支付
创建    : 2022-05-27 20:16
更新    : 2022-05-27 20:16
编写    : 陈倚云
"""


class WechatPay:
    """
    微信支付类
    """

    def __init__(self,
                 pay_type,
                 mchid,
                 key_dir,
                 cert_serial_no,
                 appid,
                 apiv3_key,
                 notify_url=None,
                 ):
        """
        :param pay_type: 微信支付类型，示例值:WeChatPayType.MINIPROG
        :param mchid: 直连商户号，示例值:'1230000109'
        :param key_dir: 商户证书私钥路径
        :param cert_serial_no: 商户证书序列号，示例值:'444F4864EA9B34415...'
        :param appid: 应用ID，示例值:'wxd678efh567hg6787'
        :param apiv3_key: 商户APIv3密钥，示例值:'a12d3924fd499edac8a5efc...'
        :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
        """
        from .build import Build

        self._type = pay_type
        self._mchid = mchid
        self._appid = appid
        self._notify_url = notify_url
        self._build = Build(mchid=self._mchid,
                            cert_serial_no=cert_serial_no,
                            key_dir=key_dir,
                            apiv3_key=apiv3_key,
                            )

    @staticmethod
    def get_private_key(mch_key):
        """
        获取私钥
        """
        with open(file=mch_key) as fh:
            p_key = fh.read()
        return p_key

    def callback(self, request):
        """解密回调接口收到的信息，返回所有传入的参数
        :param request: 回调接口收到的headers
        """
        headers = {
            'Wechatpay-Signature': request.META.get('HTTP_WECHATPAY_SIGNATURE', None),  # 应答签名
            'Wechatpay-Timestamp': request.META.get('HTTP_WECHATPAY_TIMESTAMP', None),  # 应答时间戳
            'Wechatpay-Nonce': request.META.get('HTTP_WECHATPAY_NONCE', None),  # 应答随机串
            'Wechatpay-Serial': request.META.get('HTTP_WECHATPAY_SERIAL', None)  # 应答随机串
        }
        body = request.body
        return self._build.callback(headers, body)

    from .transaction import (place, close, query, refund, query_refund, trade_bill, fundflow_bill, download_bill)
