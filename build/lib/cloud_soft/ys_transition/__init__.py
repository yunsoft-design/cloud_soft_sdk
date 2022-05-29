#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 转换类
创建    : 2022-05-29 8:28
更新    : 2022-05-29 8:28
编写    : 陈倚云
"""
import ast


class YsTransition(object):
    """
    云软转换类
    """

    @staticmethod
    def str_to_dict(str_obj):
        """
        字符串转字典
        """
        dct_obj = ast.literal_eval(str_obj)
        return dct_obj

    @staticmethod
    def unicode_decode(uni_str):
        """
        unicode转码
        """
        return uni_str.encode('utf-8').decode("unicode_escape")

    @staticmethod
    def dec_to_sixty_two(num):
        """
        十进制转62进制
        """
        all_chars = '0123456789ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
        digits = []
        while num > 0:
            # 拿到对应的下标取得62进制数，并插入列表0号位
            digits.insert(0, all_chars[num % 62])
            num //= 62
        return ''.join(digits)

    @staticmethod
    def sixty_two_to_dec(s62):
        """
        62进制转十进制
        """
        all_chars = '0123456789ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
        num = 0
        for i, s in enumerate(s62):
            pos = all_chars.rfind(s)
            num = num * 62 + pos
        return num

    @staticmethod
    def standard_str(in_str):
        """
        标准化上传字符串
        :param in_str: 上传字符串
        :return:
        """
        if in_str is None:
            return None
        out_str = None if len(str(in_str).strip()) == 0 else str(in_str).strip()
        return out_str

    @staticmethod
    def standard_int(in_int):
        """
        标准化上传整数
        :param in_int: 整数
        :return:
        """
        if in_int is None:
            return None
        out_int = None if len(str(in_int).strip()) == 0 else int(str(in_int).strip())
        return out_int
