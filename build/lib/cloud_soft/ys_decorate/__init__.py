#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 装饰函数
创建    : 2022-05-29 8:53
更新    : 2022-05-29 8:53
编写    : 陈倚云
"""
import json
from django.views.generic import View
from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
from ..ys_exception import YsException


# 装饰函数
def rate_limit(code, rate):  # 传入参数
    """
    外部函数
    """

    def func_limit(func):  # 传入函数
        """
        限制函数
        """

        def wrapper(cls, request, *args, **kwargs):
            """
            包装函数
            """
            if request.META.get('HTTP_X_FORWARDED_FOR', None):
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
            else:
                ip = request.META.get('REMOTE_ADDR')
            conn = get_redis_connection('limit_count')
            key_word = code + '/' + ip
            content = conn.get(key_word)
            if int(conn.ttl(key_word)) > rate - 2:
                conn.expire(key_word, rate)
                return YsException('访问太过频繁')
            if content is not None:
                conn.expire(key_word, rate)
                rec_dct = json.loads(content)
                # 查询成功,返回结果
                return rec_dct
            else:
                return func(cls, request, *args, **kwargs)

        return wrapper

    return func_limit


class LimitVisit(View):
    """
    限制访问次数
    """

    @classmethod
    @rate_limit('06-03', 30)
    def get(cls, request):
        """
        测试接口
        """
        try:
            conn = get_redis_connection('limit_count')
            if request.META.get('HTTP_X_FORWARDED_FOR', None):
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
            else:
                ip = request.META.get('REMOTE_ADDR')
            ret_dct = {
                "name": "Chengl139"
            }
            key_word = '06-03/' + ip
            conn.set(key_word, json.dumps(ret_dct), 30)
            return HttpResponse(msg='查询成功')
        except Exception as e:
            return HttpResponse('查询失败'+str(e))