#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : menu.py
标题    : 公众号菜单
创建    : 2022-05-27 18:43
更新    : 2022-05-27 18:43
编写    : 陈倚云
"""
import json
import requests


class Menu(object):
    """
    自定义菜单
    """

    def __init__(self, access_token):
        self._access_token = access_token

    def sql_menu(self):
        """
        查询菜单
        """
        wechat_url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + self._access_token
        res = requests.get(url=wechat_url)
        return json.loads(res.content)

    def create_menu(self, menu_dct):
        """
        创建菜单
        """
        menu_dct = json.dumps(menu_dct, ensure_ascii=False).encode('utf-8').decode('latin1')
        wechat_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + self._access_token
        res = requests.post(url=wechat_url, data=menu_dct)
        return json.loads(res.content)

    def del_menu(self):
        """
        删除菜单
        """
        wechat_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=' + self._access_token
        res = requests.get(url=wechat_url)
        return json.loads(res.content)
