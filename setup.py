#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : setup.py
标题    : 云软华为obs_SDK
创建    : 2022-05-23 0:18
更新    : 2022-05-23 0:18
编写    : 陈倚云
"""
from setuptools import setup

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="ys-cloudsoft-sdk",
    version="1.0.0",
    author="陈倚云",
    description="云软Django SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="python sdk yunsoft cloudsoft api 云软SDK",
    url="https://github.com/yunsoft-design/yr-design",
    packages=["cloud_soft"],
    classifiers=[
        "Natural Language :: 简体中文"  # 支持语言
        "Development Status :: 5 - Production/Stable",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3.8.2",  # Python版本
    ],
    install_requires=[
        "backports.zoneinfo==0.2.1",
        "tzdata==2022.1",
        "sqlparse==0.4.2",
        "asgiref==3.5.2",
        "xlwt==1.3.0",
        "xlrd==2.0.1",
        "requests==2.27.1",
        "pinyin==0.4.0",
        "itsdangerous==2.1.2",
        "six==1.16.0",
        "xmltodict==0.13.0",
        "pycryptodome==3.14.1",
        "cryptography==37.0.2",
        "mysqlclient==2.1.0",
        "django_redis==4.0.0",
        "django-cors-headers==3.12.0",
        "django==4.1a1",
        "pytz==2022.1",
    ],
)

"""
    编译  python setup.py build
    打包  python setup.py sdist
    安装  python setup.py install
    重新安装 pip install D:\cloud_soft_sdk\dist\ys-cloudsoft-sdk-1.0.0.tar.gz --force-reinstall
"""