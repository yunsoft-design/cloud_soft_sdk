#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 华为obs类
创建    : 2022-05-29 8:36
更新    : 2022-05-29 8:36
编写    : 陈倚云
"""
import base64
import http.client as httplib
from obs import ObsClient
from ..ys_exception import YsException
from ..ys_date import YsDate

class YsObserver(object):
    """
    华为obs服务扩展接口
    """

    def __init__(self, access_key, secret_access_key, server_url, bucket_name):
        self._client = ObsClient(
            access_key_id=access_key,
            secret_access_key=secret_access_key,
            server=server_url
        )
        self._bucket_name = bucket_name

    @staticmethod
    def parse_url(url):
        """
        解析URL字符串
        :param url:
        :return:
        """
        temp = url.partition('://')
        head = temp[0].upper()  # HTTPS or HTTP
        temp = temp[-1].partition('/')[0]  # wx.qlogo.cn:443
        domain = temp.partition(':')[0]  # wx.qlogo.cn
        port = temp.partition(':')[-1]  # 443
        if not port.strip():
            if head == 'HTTPS':
                port = '443'
            else:
                port = '80'
        return head, domain, port

    def get_obs_url(self, object_name, expires=60 * 60, inter=''):
        """
        功能：根据桶名和文件名，动态生成访问文件的url
        object_key:OBS上存储的文件名
        """
        try:
            res = self._client.createSignedUrl('GET', self._bucket_name, object_name, expires=expires)
            return res['signedUrl']
        except Exception as e:
            raise YsException(inter, '获取obs url失败', e)

    def url_upload(self, url):
        """
        功能：根据图片url,下载图片并上传到为OBS
        url:微信头像的url
        flag:每个桶的编号
        返回：文件名即可(因url加密，每次url不一样,故数据库只能需要保存文件名,然后，根据文件名动态生成每次访问的url)
        """
        try:
            if url is None:
                return ''
            head, domain, port = self.parse_url(url)
            if head == 'HTTPS':
                conn = httplib.HTTPSConnection(host=domain, port=port)
            else:
                conn = httplib.HTTPConnection(host=domain, port=port)
            conn.request('GET', url)
            content = conn.getresponse()
            object_name = YsDate.get_timestamp() + '.jpg'
            self._client.putContent(self._bucket_name, object_name, content=content)
            return object_name
        except Exception as e:
            raise YsException('下载图片上传到obs', '失败', e)

    def file_upload(self, file_path):
        """
        直接从后台上传文件
        :param file_path: 包括文件全路径及文件名
        :return:
        """
        try:
            object_name = YsDate.get_timestamp()
            extend = str(file_path).split('.')
            if len(extend) > 0:
                object_name += '.' + extend[-1]
            self._client.putFile(self._bucket_name, object_name, file_path)
            return object_name
        except Exception as e:
            raise YsException('后台上传文件', '失败', e)

    def base64_upload(self, content):
        """
        图片BASE64上传
        :param content:BASE64
        :return:
        """
        try:
            object_name = YsDate.get_timestamp() + '.jpg'
            self._client.putContent(self._bucket_name, object_name, content=content)
            return object_name
        except Exception as e:
            raise YsException('图片BASE64上传', '失败', e)

    def base64_down(self, object_name):
        """
        功能：根据obs_name,下载文件
        object_key:对象名,即object_name
        flag:每个桶的编号
        返回：文件base64,如果文件不存在,则返回空
        """
        try:
            resp = self._client.getObject(self._bucket_name, object_name, loadStreamInMemory=True)
            b64 = bytes(base64.b64encode(resp.body.buffer)).decode()
            return b64
        except Exception as e:
            raise YsException('下载obs文件', '失败', e)
