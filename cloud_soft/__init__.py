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
from .wechat import Wechat
from .signature import Signature


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
                 longitude=None,
                 latitude=None,
                 host=None,
                 ak=None,
                 sk=None,
                 wechat_token=None
                 ):
        """
        云软算法SDK
        :param appid:小程序或公众号appid
        :param app_secret: 小程序、公众号、短信sms secret、华为隐私电话sk
        :param redis_alias: 访问令牌存放的redis别名
        :param observer: obs对象
        :param sms_url: 华为短信SMS接入地址(在控制台"应用管理"页面获取)+接口访问URI
        :param appkey: 华为短信SMS appkey;高德地图appkey;华为隐私电话appkey
        :param sender: 华为短信SMS # 国内短信签名通道号或国际/港澳台短信通道号
        :param template_id: 华为短信SMS 短信模板
        :param longitude: 高德经度
        :param latitude: 高德纬度
        :param host: 华为隐私电话服务器IP
        :param ak: 华为隐私电话ak
        :param sk: 华为隐私电话sk
        :param wechat_token: 微信设置的token
        """
        self.applet = Applet(appid, app_secret, redis_alias, observer)
        self.token = YsToken(secret_key, salt)
        self.sms = YsSms(
            url=sms_url,
            appkey=appkey,
            app_secret=app_secret,
            sender=sender,
            template_id=template_id,
            redis_alias=redis_alias
        )
        self.location = Location(
            api_key=appkey,
            longitude=longitude,
            latitude=latitude
        )
        self.private_tel = PrivateTel(
            app_key=appkey,
            host=host,
            ak=ak,
            sk=sk,
        )
        self.wechat = Wechat(
            appid=appid,
            secret=app_secret,
            token=wechat_token
        )

    from .date import YsDate
    from .decorate import rate_limit
    from .observer import Observer
    from .exception import YsException
    from .regular import Regular
    from .character import Character
    from .transition import Transition
    from .signature import Signature
    from .payment import WechatPay
    from .interaction import BackendToFront, FrontToBackend
