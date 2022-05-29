#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : qr_code.py
标题    : 生成二维码
创建    : 2022-05-27 12:20
更新    : 2022-05-27 12:20
编写    : 陈倚云
"""

import requests


class QrCode:
    """
    获取二维码
    """

    def __init__(self, access_token, observer):
        self._access_token = access_token
        self._observer = observer

    def create_qrcode_a(self, path):
        """
        接口A：适用于需要的码数量较少,10万个以内的业务场景.可接受path较长
        文档：https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/qr-code.html
        """
        url = 'https://api.weixin.qq.com/wxa/getwxacode?access_token=' + self._access_token
        data = {
            # "path": "src/pages/mine/login?type=join&org_id=" + scene,
            "path": path,
            "width": 430,
            "auto_color": False,
            "line_color": {"r": 163, "g": 0, "b": 0},  # 自定义颜色 auto_color 为 false 时生效
            # "line_color": {"r": 233, "g": 195, "b": 65},  # 自定义颜色
            "is_hyaline": True  # 是否需要透明底色
        }
        ret = requests.post(url, json=data)
        qr_url = self._observer.base64_upload(ret.content)
        return qr_url

    def create_qrcode_b(self, path, scene):
        """
        接口B：适用于需要的码数量极多的业务场景
        文档：https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/qr-code.html
        org_id:机构id
        path:小程序路径
        applet_num:小程序编号
        """
        url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + self._access_token
        data = {
            "path": path,
            "scene": scene,
            "width": 430,
            "line_color": {"r": 163, "g": 0, "b": 0},  # 自定义颜色
            "is_hyaline": True
        }
        ret = requests.post(url, json=data)
        qr_url = self._observer.base64_upload(ret.content)
        return qr_url

    def create_qrcode_c(self, path):
        """
        接口C：适用于需要的码数量较少,10万个以内的业务场景。可接受path参数较长
        """
        url = 'https://api.weixin.qq.com/cgi-bin/wxaapp/createwxaqrcode?access_token=' + self._access_token
        data = {
            "path": path,
            "width": 430
        }
        ret = requests.post(url, json=data)
        qr_url = self._observer.base64_upload(ret.content)
        return qr_url
