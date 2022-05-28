#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 云软算法SDK
创建    : 2022-05-27 9:05
更新    : 2022-05-27 9:05
编写    : 陈倚云
"""

from .applet import Applet
from .decorate import rate_limit
from .token import YsToken
from .sms import YsSms
from .location import Location
from .privte_tel import PrivateTel


class CloudSoft:
    """
    云软算法SDK
    """

    def __init__(self,
                 appid=None,
                 app_secret=None,
                 redis_alias=None,
                 observer=None,
                 secret_key=None,
                 salt=None,
                 sms_url=None,
                 appkey=None,
                 sender=None,
                 template_id=None,
                 host=None,
                 ak=None,
                 sk=None,
                 wechat_token=None,
                 pay_type=None,
                 mchid=None,
                 key_dir=None,
                 cert_serial_no=None,
                 apiv3_key=None,
                 notify_url=None
                 ):
        """
        云软算法SDK
        :param appid:小程序、公众号appid
        :param app_secret: 小程序、公众号、短信sms secret、华为隐私电话sk
        :param redis_alias: 访问令牌存放的redis别名
        :param observer: obs对象
        :param sms_url: 华为短信SMS接入地址(在控制台"应用管理"页面获取)+接口访问URI
        :param appkey: 华为短信SMS appkey;高德地图appkey;华为隐私电话appkey
        :param sender: 华为短信SMS # 国内短信签名通道号或国际/港澳台短信通道号
        :param template_id: 华为短信SMS 短信模板
        :param host: 华为隐私电话服务器IP
        :param ak: 华为隐私电话ak
        :param sk: 华为隐私电话sk
        :param wechat_token: 微信设置的token
        :param pay_type: 微信支付类型
        :param mchid: 微信支付 直连商户号，示例值:'1230000109'
        :param key_dir: 商户证书私钥路径
        :param cert_serial_no: 商户证书序列号，示例值:'444F4864EA9B34415...'
        :param apiv3_key: 商户APIv3密钥，示例值:'a12d3924fd499edac8a5efc...'
        :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
        """
        if appkey is not None and app_secret is not None and redis_alias is not None and observer is not None:
            self.applet = Applet(appid, app_secret, redis_alias, observer)
        if secret_key is not None and salt is not None:
            self.token = YsToken(secret_key, salt)
        if sms_url is not None:
            self.sms = YsSms(
                url=sms_url,
                appkey=appkey,
                app_secret=app_secret,
                sender=sender,
                template_id=template_id,
                redis_alias=redis_alias
            )
        if appkey is not None:
            self.location = Location(
                api_key=appkey,
            )
        if ak is not None:
            self.private_tel = PrivateTel(
                app_key=appkey,
                host=host,
                ak=ak,
                sk=sk,
            )
        if wechat_token is not None:
            from .wechat import Wechat
            self.wechat = Wechat(
                appid=appid,
                secret=app_secret,
                token=wechat_token
            )
        from .signature import Signature
        self.signature = Signature()
        if pay_type is not None:
            from .payment import WechatPay
            self.wechat_pay = WechatPay(
                pay_type=pay_type,
                mchid=mchid,
                key_dir=key_dir,
                cert_serial_no=cert_serial_no,
                appid=appid,
                apiv3_key=apiv3_key,
                notify_url=notify_url
            )

    from .date import YsDate
    from .decorate import rate_limit
    from .observer import Observer
    from .exception import YsException
    from .regular import Regular
    from .character import Character
    from .transition import Transition

    from .interaction import BackendToFront, FrontToBackend
