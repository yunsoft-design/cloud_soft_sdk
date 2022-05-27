#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : service.py
标题    : 微信客服
创建    : 2022-05-27 18:47
更新    : 2022-05-27 18:47
编写    : 陈倚云
"""
import json
import requests


class Service(object):
    """
    客服管理
    """

    def __init__(self, access_token):
        self._access_token = access_token

    def get_lst(self):
        """
        查询客服列表
        """
        wechat_url = 'https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token=' + self._access_token
        res = requests.get(url=wechat_url)
        return json.loads(res.content)

    def add(self,kf_account, nickname):
        """
        添加客服账号
        """
        wechat_url = 'https://api.weixin.qq.com/customservice/kfaccount/add?access_token=' + self._access_token
        params = {
            "kf_account": kf_account + "@yiwenzhen365",
            "nickname": nickname
        }
        params = json.dumps(params, ensure_ascii=False).encode('utf-8').decode('latin1')
        res = requests.post(url=wechat_url, data=params)
        return json.loads(res.content)

    def bind(self,kf_account, invite_wx):
        """
        邀请客服绑定账号
        """
        wechat_url = 'https://api.weixin.qq.com/customservice/kfaccount/inviteworker?access_token=' + self._access_token
        params = {
            "kf_account": kf_account,
            "invite_wx": invite_wx
        }

        res = requests.post(url=wechat_url, json=params)
        return json.loads(res.content)

    def del_account(self,kf_account):
        """
        删除客户账号
        """
        wechat_url = 'https://api.weixin.qq.com/customservice/kfaccount/del?access_token=' + self._access_token + '&kf_account=' + kf_account
        res = requests.get(url=wechat_url)
        return json.loads(res.content)

    @staticmethod
    def invit(from_user, to_user):
        """
        转发消息到客服
        """
        ret_xml = "<xml><ToUserName><![CDATA[" + to_user + \
                  "]]></ToUserName><FromUserName><![CDATA[" + from_user + "]]></FromUserName><CreateTime>1399197672</CreateTime><MsgType><![CDATA[transfer_customer_service]]></MsgType></xml>"
        return ret_xml
