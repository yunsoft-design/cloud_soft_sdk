#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : user.py
标题    : 微信用户
创建    : 2022-05-27 18:48
更新    : 2022-05-27 18:48
编写    : 陈倚云
"""
import json
import requests


class User(object):
    """
    用户管理
    """

    def __init__(self, access_token):
        self._access_token = access_token

    def get_lst(self, next_openid=None):
        """
        获取用户列表
        """
        if next_openid:
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=' + self._access_token + '&next_openid=' + next_openid
        else:
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=' + self._access_token
        res = requests.get(url=wechat_url)
        return json.loads(res.content)

    def get_info(self, user_lst):
        """
        获取用户基本信息
        """
        wechat_url = 'https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=' + self._access_token
        res = requests.post(url=wechat_url, json=user_lst)
        return json.loads(res.content)

    def remark(self, remark_dct):
        """
        设置用户备注
        """
        wechat_url = 'https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token=' + self._access_token
        params = json.dumps(remark_dct, ensure_ascii=False).encode('utf-8').decode('latin1')
        res = requests.post(url=wechat_url, data=params)
        return json.loads(res.content)
