#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 
创建    : 2022-05-29 8:27
更新    : 2022-05-29 8:27
编写    : 陈倚云
"""
import re
class YsRegular(object):
    """
    云软验证类
    """

    @staticmethod
    def mobile_is_valid(phone_str):
        """
        验证手机号是否合法
        """
        if re.match(r'1[3,4,5,7,8]\d{9}', phone_str):
            return 1
        else:
            return 0

    @staticmethod
    def obs_file_name_is_valid(file_name):
        """
        验证obs文件名是否合法
        """
        if re.match(r'^[0-9]{18}\.jpg$', file_name):
            return 1
        else:
            return 0

    @staticmethod
    def cert_is_valid(cert_id):
        """
        验证身份证
        """
        if re.match(r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}[0-9Xx]$)', cert_id):
            return 1
        else:
            return 0