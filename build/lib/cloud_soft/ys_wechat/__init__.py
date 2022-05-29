#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 
创建    : 2022-05-27 18:51
更新    : 2022-05-27 18:51
编写    : 陈倚云
"""
import hashlib
import requests
import six
import json
import xmltodict
from ..ys_exception import YsException
from django_redis import get_redis_connection
from .menu import Menu
from .reply import Replay
from .service import Service
from .user import User
from ..ys_date import YsDate
from ..ys_transition import YsTransition


def to_text(value, encoding='utf-8'):
    """
    把decode文本转换为文本
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


class YsWechat(object):
    """
    公众号相关接口
    """

    # WECHAT_TOKEN = 'cloud_soft'
    # WECHAT_APPID = 'wx437dc69c66322e0c'
    # WECHAT_APPSECRET = 'b12d380d6956f48c959d65d97c868dd1'
    def __init__(self, token, appid, secret, redis_alias):
        """
        :param token: 公众平台设置的token
        :param appid: 公众平台appid
        :param secret: 公众平台app_secret
        """
        self._token = token
        self._appid = appid
        self._secret = secret
        self._redis_alias = redis_alias
        self._expire = 10
        self._access_token = self.get_access_token()
        self.menu = Menu(self._access_token)
        self.reply = Replay(self._access_token, appid)
        self.service = Service(self._access_token)
        self.user = User(self._access_token)

    def verify_message(self, signature, timestamp, nonce, echostr):
        """
        验证消息确实来源于微信服务器
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Access_Overview.html
        """
        if not all([signature, timestamp, nonce, echostr]):
            raise YsException(errmsg='请求参数错误')
        # 1 将token、timestamp、nonce三个参数进行字典序排序
        tmp_str = "".join(sorted([self._token, timestamp, nonce]))
        # 2 将三个参数字符串拼接成一个字符串进行sha1加密
        tmp_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
        # 3 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
        if tmp_str == signature:
            return echostr
        else:
            return False

    def get_access_token(self):
        """
        获取公众access_token
        """
        conn = get_redis_connection(self._redis_alias)
        access_token = conn.get(self._appid)
        if access_token is None or bytes(access_token).decode() == 'None':
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self._appid + '&secret=' + self._secret
            res = requests.get(url=wechat_url)
            ret = json.loads(res.content)
            access_token = ret.get('access_token', None)
            conn.set(self._appid, access_token, self._expire)
        else:
            access_token = bytes(access_token).decode()
        return access_token

    @staticmethod
    def parse(xml):
        """
            解析微信服务器推送的 XML 消息

            :param xml: XML 消息
            :return: 解析成功返回对应的消息或事件，否则返回 ``UnknownMessage``
            """
        if not xml:
            return
        message = xmltodict.parse(to_text(xml))['xml']
        return message


    class Blacklist(object):
        """
        黑名单管理
        """

        @staticmethod
        def get_lst(next_openid=None):
            """
            获取黑名单列表
            """
            next_openid = '' if next_openid is None else next_openid
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/tags/members/getblacklist?access_token=' + Wechat.get_access_token()
            parames = {
                'begin_openid': next_openid
            }
            res = requests.post(url=wechat_url, json=parames)
            return json.loads(res.content)

        @staticmethod
        def set_blacklist(openid_list):
            """
            获取黑名单列表
            """
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchblacklist?access_token=' + Wechat.get_access_token()
            parames = {
                'openid_list': openid_list
            }
            res = requests.post(url=wechat_url, json=parames)
            return json.loads(res.content)

        @staticmethod
        def cancel_blacklist(openid_list):
            """
            取消拉黑
            """
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchunblacklist?access_token=' + Wechat.get_access_token()
            parames = {
                'openid_list': openid_list
            }
            res = requests.post(url=wechat_url, json=parames)
            return json.loads(res.content)

    class Ocr(object):
        """
        ocr图片识别
        """

        @staticmethod
        def identification(card_type, url):
            """
            图片识别
            """
            wechat_url = ''
            if card_type == 1:  # 身份证识别
                wechat_url = 'https://api.weixin.qq.com/cv/ocr/idcard?img_url=' + url + '&access_token=' + Wechat.get_access_token()
            elif card_type == 2:  # 银行卡识别
                wechat_url = 'https://api.weixin.qq.com/cv/ocr/bankcard?img_url=' + url + '&access_token=' + Wechat.get_access_token()
            elif card_type == 3:  # 行驶证识别
                wechat_url = 'https://api.weixin.qq.com/cv/ocr/driving?img_url=' + url + '&access_token=' + Wechat.get_access_token()
            elif card_type == 4:  # 驾驶证识别
                wechat_url = 'https://api.weixin.qq.com/cv/ocr/drivinglicense?img_url=' + url + '&access_token=' + Wechat.get_access_token()
            elif card_type == 5:  # 营业执照识别
                wechat_url = 'https://api.weixin.qq.com/cv/ocr/bizlicense?img_url=' + url + '&access_token=' + Wechat.get_access_token()
            elif card_type == 6:  # 车牌识别
                wechat_url = 'https://api.weixin.qq.com/cv/ocr/platenum?img_url=' + url + '&access_token=' + Wechat.get_access_token()
            res = requests.post(wechat_url)
            return json.loads(res.content)

    class Template(object):
        """
        模板管理
        """

        @staticmethod
        def send(data):
            """
            发送订阅通知
            """
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/bizsend?access_token=' + Wechat.get_access_token()
            parames = json.dumps(data, ensure_ascii=False).encode('utf-8').decode('latin1')
            res = requests.post(url=wechat_url, data=parames)
            return json.loads(res.content)

    class QrCode(object):
        """
        获取带参二维码
        """

        @staticmethod
        def get(user_info_id,observer):
            """
            获取带参临时二维码
            :param user_info_id: 用户id
            :param observer: obs对象
            :return:
            """
            conn = get_redis_connection('qr_code')
            file = conn.get('file_' + str(user_info_id))
            if file is None or bytes(file).decode() == 'None':
                wechat_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=' + Wechat.get_access_token()
                params = {
                    "expire_seconds": 2592000,
                    "action_name": "QR_SCENE",
                    "action_info": {
                        "scene": {
                            "scene_id": user_info_id
                        }
                    }
                }
                res = requests.post(url=wechat_url, json=params)
                ret = json.loads(res.content)
                ticket = ret['ticket']
                wechat_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + ticket
                res = requests.get(url=wechat_url)
                file = observer.base64_upload(res.content)
                # qr_code = ret.get('qr_code', None)
                conn.set('file_' + str(user_info_id), file)
                conn.expire('file_' + str(user_info_id), 2591000)
            else:
                file = bytes(file).decode()
            url = observer.get_obs_url(file)
            return url

    class Article(object):
        """
        文章管理
        """

        @staticmethod
        def get_lst(info):
            """
            获取文章列表
            """
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=' + Wechat.get_access_token()
            res = requests.post(url=wechat_url, json=info)
            articles = json.loads(res.content)
            article_lst = []
            for article in articles['item']:
                article_lst.append({
                    'media_id': article['media_id'],
                    'title': YsTransition.unicode_decode(article['content']['news_item'][0]['title']),
                    'author': YsTransition.unicode_decode(article['content']['news_item'][0]['author']),
                    'digest': YsTransition.unicode_decode(article['content']['news_item'][0]['digest']),
                    'content': YsTransition.unicode_decode(article['content']['news_item'][0]['content']),
                    'content_source_url': article['content']['news_item'][0]['content_source_url'],
                    'thumb_media_id': article['content']['news_item'][0]['thumb_media_id'],
                    'show_cover_pic': article['content']['news_item'][0]['show_cover_pic'],
                    'url': article['content']['news_item'][0]['url'],
                    'thumb_url': article['content']['news_item'][0]['thumb_url'],
                    'need_open_comment': article['content']['news_item'][0]['need_open_comment'],
                    'only_fans_can_comment': article['content']['news_item'][0]['only_fans_can_comment'],
                    'create_time': YsDate.timestamp_to_time(article['content']['create_time']),
                    'update_time': YsDate.timestamp_to_time(article['content']['update_time']),
                })
            return article_lst

        @staticmethod
        def update(media_id, articles):
            """
            更新文章
            """
            if media_id is None:
                wechat_url = 'https://api.weixin.qq.com/cgi-bin/draft/add?access_token=' + Wechat.get_access_token()
                res = requests.post(url=wechat_url, json=articles)
                info = json.loads(res.content)
                return info['media_id']
            else:
                wechat_url = 'https://api.weixin.qq.com/cgi-bin/draft/add?access_token=' + Wechat.get_access_token()
                res = requests.post(url=wechat_url, json=articles)
                info = json.loads(res.content)
                return info['media_id']

        @staticmethod
        def delete(media_id):
            """
            删除文章
            """
            wechat_url = 'https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=' + Wechat.get_access_token()
            params = {
                "media_id": media_id
            }
            res = requests.post(url=wechat_url, json=params)
            return json.loads(res.content)
