#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : reply.py
标题    : 公众号回复
创建    : 2022-05-27 18:44
更新    : 2022-05-27 18:44
编写    : 陈倚云
"""
import json
import requests
from ..ys_date import YsDate


class Replay(object):
    """
    消息回复
    """

    def __init__(self, access_token, appid):
        """
        微信回复
        :param access_token: 微信令牌
        :param appid: 微信appid
        """
        self._access_token = access_token
        self._appid = appid

    def reply_miniprogrampage(self, openid, url):
        """
        发送跳转到小程序的消息
        """
        wechat_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + self._access_token
        params = {
            "touser": openid,
            "msgtype": "miniprogrampage",
            "miniprogrampage":
                {
                    # "title": "",
                    "appid": self._appid,
                    "pagepath": url,
                    "thumb_media_id": '6ZmOiIg1K88ja9lOX86AbLFz-OMOZKkH4yIxhvH72hCo5ehzo8M68A0-NR6CXDGO'
                }
        }
        res = requests.post(url=wechat_url, json=params)
        return json.loads(res.content)

    @staticmethod
    def text(from_user, to_user, content):
        """
        消息转发至客服
        """
        ret_xml = "<xml><ToUserName><![CDATA[" + \
                  to_user + \
                  "]]></ToUserName><FromUserName><![CDATA[" + \
                  from_user + "]]></FromUserName><CreateTime>" + \
                  YsDate.get_timestamp() + "</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[" + \
                  content + "]]></Content></xml>"
        return ret_xml

    @staticmethod
    def article(from_user, to_user, articles):
        """
        回复图文消息
        """
        ret_xml1 = "<xml><ToUserName><![CDATA[" + to_user + \
                   "]]></ToUserName><FromUserName><![CDATA[" + from_user + \
                   "]]></FromUserName><CreateTime>" + YsDate.get_timestamp() + \
                   "</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>" + str(len(articles)) + "</ArticleCount><Articles>"
        ret_xml2 = ""
        for article in articles:
            ret_xml2 += "<item><Title><![CDATA[" + article["title"] + \
                        "]]></Title><Description><![CDATA[" + article["description"] + \
                        "]]></Description><PicUrl><![CDATA[" + article["image"] + \
                        "]]></PicUrl><Url><![CDATA[" + article["url"] + "]]></Url></item>"
        ret_xml3 = "</Articles></xml>"
        ret_xml = ret_xml1 + ret_xml2 + ret_xml3
        return ret_xml
