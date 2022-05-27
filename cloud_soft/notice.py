#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : notice.py
标题    : 
创建    : 2022-05-27 15:15
更新    : 2022-05-27 15:15
编写    : 陈倚云
"""
import datetime
import json
import requests


class Notice:
    """
    发送消息
    """

    def __init__(self, access_token):
        self._access_token = access_token

    def send_post_audit_msg(self, openid, result, content):
        """
        用户申请岗位：审核结果通知->通知用户
        """
        # user = UserInfo.objects.get(id=user_id)
        # openid = user.user_info_find_user_applet.get(applet=1).openid
        url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + self._access_token
        request_date = {
            "touser": openid,
            "template_id": "g-b9ONp9sWHB0J8rCmrfHMqfaaKVv0Ph_jgHpdLXe-o",
            "page": "/src/pages/mine/login?type=organization",
            "data": {
                "date2": {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                "name3": {"value": '组织管理员'},
                "thing1": {"value": '岗位授权'},
                "phrase5": {"value": result},
                "thing10": {"value": content}
            }
        }
        ret = requests.post(url, json=request_date)
        res = json.loads(ret.content)
        # print(res)
        if res["errmsg"] == "ok" and res['errcode'] == 0:
            return 1
        else:
            return 0

    def send_user_request_msg(self, openid, real_name, post_name):
        """
        用户申请岗位：用户申请通知->通知管理员
        :openid:管理员openid
        """
        # user = UserInfo.objects.get(id=manage_id)
        # openid = user.user_info_find_user_applet.get(applet=1).openid
        # access_token = cls.get_access_token(1)
        url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + self._access_token
        request_date = {
            "touser": openid,
            "template_id": "T8H_5s9kRJcERixrk9CaKbQkN6gvbNqj4FE7F0ApVA4",
            "page": "/src/pages/mine/login?type=organization",
            "data": {
                "name1": {"value": real_name},
                "thing2": {"value": post_name},
                "time3": {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            }
        }
        ret = requests.post(url, json=request_date)
        res = json.loads(ret.content)
        print(res)
        if res["errmsg"] == "ok" and res['errcode'] == 0:
            return 1
        else:
            return 0

    def send_org_request_msg(self, short_name, real_name):
        """
        组织入驻申请通知->通知客服
        """
        # openid = user.user_info_find_user_applet.get(applet=1).openid
        url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + self._access_token
        request_date = {
            "touser": "o2b6b5S9vJPVSRMcNtEHuianAga0",  # user_applet表中,applet=时的user_id
            "template_id": "tcKHX-LxFg0j2bifH-gZbTHxT10atQaLMwDdfCKgDLA",
            "page": "/src/pages/mine/login?type=organization",
            "data": {
                "name1": {"value": short_name},
                "name2": {"value": real_name},
                "time3": {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            }
        }
        ret = requests.post(url, json=request_date)
        res = json.loads(ret.content)
        if res["errmsg"] == "ok" and res['errcode'] == 0:
            return 1
        else:
            return 0

    def send_org_audio_msg(self, openid, state_str, comment):
        """
        组织入驻审核结果通知->通知组织创建者
        """
        # user = org.manager
        # openid = user.user_info_find_user_applet.get(applet=1).openid
        # access_token = cls.get_access_token(1)
        url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + self._access_token
        request_date = {
            "touser": openid,
            "template_id": "g-b9ONp9sWHB0J8rCmrfHImXQ_fpD4BisfrBAK2azMQ",
            "page": "/src/pages/mine/login?type=organization",
            "data": {
                # "thing18": {"value": org.short_name},
                # "thing16": {"value": user.real_name},
                "phrase8": {"value": state_str},
                "thing10": {"value": comment},
                "date2": {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            }
        }
        ret = requests.post(url, json=request_date)
        res = json.loads(ret.content)
        if res["errmsg"] == "ok" and res['errcode'] == 0:
            return 1
        else:
            return 0
