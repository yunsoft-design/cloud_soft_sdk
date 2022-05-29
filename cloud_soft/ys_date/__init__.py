#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 日期类
创建    : 2022-05-29 8:37
更新    : 2022-05-29 8:37
编写    : 陈倚云
"""
import datetime
import time


class YsDate(object):
    """
    云软日期类
    """

    @staticmethod
    def get_timestamp():
        """
        获取时间戳
        :return:
        """
        timestamp = str(int(time.time() * 10000))
        return timestamp

    @staticmethod
    def timestamp_to_time(timestamp):
        """
        时间戳转时间
        """
        time_array = time.localtime(int(timestamp) / 10000)
        return time.strftime('%Y-%m-%d %H:%M:%S', time_array)

    @staticmethod
    def is_leap_year(year):
        """
        确定某一年是否是润年
        """
        year = int(year)
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            return 1
        else:
            return 0

    @staticmethod
    def get_total_days(str_date):
        """
        计算某个日期到公元元年一月一日的总天数
        :param str_date: 日期字符串
        :return:
        """
        p_date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
        year = p_date.year
        month = p_date.month
        day = p_date.day
        days = 0
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if YsDate.is_leap_year(year):
            month_days[1] = 29
        for i in range(1, year):
            year_day = 365
            if YsDate.is_leap_year(i):
                year_day = 366
            days += year_day
        for m in range(month - 1):
            days += month_days[m]
        days += day
        return days

    @staticmethod
    def wechat_time(time_str, fmt):
        """
        生成微信日期格式
        """
        cur_time = datetime.datetime.now()
        cur_year = cur_time.year
        cur_month = cur_time.month
        str_time = datetime.datetime.strptime(time_str, fmt)
        if str_time.year == cur_year:
            if str_time.month == cur_month:
                days_interval = (cur_time.day - str_time.day)
                if days_interval == 0:
                    result = str_time.strftime("%H:%M")
                elif days_interval == 1:
                    result = str_time.strftime("昨天 %H:%M")
                else:
                    if cur_time.strftime("%W") == str_time.strftime("%W"):
                        week_str = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
                        str_week_no = str_time.isoweekday()  # 这边要改成isoweekday方法
                        if str_week_no == 0:
                            result = str_time.strftime("%m月%d日 %H:%M")
                        else:
                            result = str_time.strftime(week_str[str_week_no] + " %H:%M")

                    else:
                        result = str_time.strftime("%m月%d日 %H:%M")
            else:
                result = str_time.strftime("%m月%d日 %H:%M")
        else:
            result = str_time.strftime("%Y年%m月%d日")
        return result
