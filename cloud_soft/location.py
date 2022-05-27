#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : location.py
标题    : 地理位置
创建    : 2022-05-27 18:01
更新    : 2022-05-27 18:01
编写    : 陈倚云
"""
import requests


class Location:
    """
    高德地图
    """

    def __init__(self, api_key, longitude, latitude):
        self._longitude = longitude
        self._latitude = latitude
        self._url = 'https://restapi.amap.com/v3/geocode/regeo?key=' + api_key + '&location=' + longitude + ',' + latitude + '&output=json&extensions=all&homeorcorp=0'

    def get(self):
        """
        获取地理位置
        """
        res = requests.get(self._url)
        answer = res.json()
        region = ''
        address = ''
        if answer['status'] == '1' and answer['info'] == 'OK':
            region_list = answer['regeocode']['addressComponent']
            region = region_list['country'] + region_list['province'] + region_list['city'] + region_list['district'] + region_list['township']
            pois_lst = answer['regeocode']['pois']
            max_i = 10000
            index = 0
            step = 1000000
            for pid, pois in enumerate(pois_lst):
                pois = str(pois['location']).split(',')
                px = int(float(pois[0]) * step)
                py = int(float(pois[1]) * step)
                xx = (pow(int(float(self._longitude) * step) - px, 2) + pow(int(float(self._latitude) * step) - py, 2)) / step
                if max_i > xx:
                    index = pid
                    max_i = xx
            address = pois_lst[index]['address']
        ret_info = {
            'longitude': self._longitude,
            'latitude': self._latitude,
            'region': region,
            'address': address
        }
        return ret_info
