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
    packages=[
        "cloud_soft"
        ".ys_applet",
        "cloud_soft.ys_character",
        "cloud_soft.ys_date",
        "cloud_soft.ys_decorate",
        "cloud_soft.ys_exception",
        "cloud_soft.ys_interaction",
        "cloud_soft.ys_location",
        "cloud_soft.ys_models",
        "cloud_soft.ys_observer",
        "cloud_soft.ys_payment",
        "cloud_soft.ys_private_tel",
        "cloud_soft.ys_regular",
        "cloud_soft.ys_crypto",
        "cloud_soft.ys_sms",
        "cloud_soft.ys_token",
        "cloud_soft.ys_transition",
        "cloud_soft.ys_wechat",
    ],
    classifiers=[
        "Natural Language :: 简体中文"  # 支持语言
        "Development Status :: 5 - Production/Stable",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3.8.2",  # Python版本
    ],
    install_requires=[
        'pycryptodome',
        'cryptography',
        'crypto',
        # 'urllib3',
        # 'pinyin',
        # 'crypto',
        # 'itsdangerous',
        # 'requests',
    ],
)

"""
    编译  python setup.py build
    打包  python setup.py sdist
    安装  python setup.py install
    重新安装 pip install D:\CloudSoftSDK\cloud_soft_sdk\dist\ys-cloudsoft-sdk-1.0.0.tar.gz --force-reinstall
"""
