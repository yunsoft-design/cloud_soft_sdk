#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 高德经纬度转地址
创建    : 2022-05-29 9:00
更新    : 2022-05-29 9:00
编写    : 陈倚云
"""
import requests


class YsLocation:
    """
    高德地图
    """

    def __init__(self, api_key):
        self._url = 'https://restapi.amap.com/v3/geocode/regeo?key=' + api_key

    def get(self, longitude, latitude):
        """
        获取地理位置
        """
        location_url = self._url + '&location=' + longitude + ',' + latitude + '&output=json&extensions=all&homeorcorp=0'
        res = requests.get(location_url)
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
                xx = (pow(int(float(longitude) * step) - px, 2) + pow(int(float(latitude) * step) - py, 2)) / step
                if max_i > xx:
                    index = pid
                    max_i = xx
            address = pois_lst[index]['address']
        ret_info = {
            'longitude': longitude,
            'latitude': latitude,
            'region': region,
            'address': address
        }
        return ret_info
