#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : transaction.py
标题    : 交易模块
创建    : 2022-04-27 6:27
更新    : 2022-04-27 6:27
编写    : 陈倚云
"""
import json
import random
import string
import time
import uuid
from .type import RequestType, PayType


def place(self, description, total, out_trade_no=None, openid=None, scene_info=None):
    """构造下单请求
    https://pay.weixin.qq.com/wiki/doc/apiv3/apis/index.shtml
    :param self: YsWechatpay类
    :param description: 商品描述
    :param total: 订单金额,以分为单位
    :param out_trade_no: 订单号
    :param openid: 支付者
    :param scene_info: 结算信息，示例值:{'profit_sharing':False}
    :return: 请求对象
    """
    params = {}
    if self._appid:
        params.update({'appid': self._appid})
    else:
        raise Exception('应用ID不存在.')
    if self._mchid:
        params.update({'mchid': self._mchid})
    else:
        raise Exception('直连商户号不存在.')
    if description:
        params.update({'description': description})
    if out_trade_no is None:
        out_trade_no = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    params.update({'out_trade_no': out_trade_no})
    if not self._notify_url:
        raise Exception('通知地址不存在.')
    params.update({'notify_url': self._notify_url})
    if total:
        params.update({'amount': {'total': total, 'currency': 'CNY'}})
    else:
        raise Exception('未输入金额.')
    if openid:
        params.update({'payer': {
            'openid': openid
        }})
    if self._type in [PayType.JSAPI, PayType.MINIPROG]:
        if not openid:
            raise Exception('支付者不存在.')
        path = '/v3/pay/transactions/jsapi'
    elif self._type == PayType.APP:
        path = '/v3/pay/transactions/app'
    elif self._type == PayType.H5:
        if not scene_info:
            raise Exception('场景信息不存在.')
        path = '/v3/pay/transactions/h5'
    elif self._type == PayType.NATIVE:
        path = '/v3/pay/transactions/native'
    else:
        raise Exception('不存在的微信支付类型')
    ret_lst = self._build.request(path, method=RequestType.POST, data=params)
    timestamp = str(int(time.time()))
    nonce_str = ''.join(str(uuid.uuid4()).split('-')).upper()
    package = 'prepay_id=' + json.loads(ret_lst[1])['prepay_id']
    data = [self._appid, timestamp, nonce_str, package]
    # print(data)
    pay_sign = self.sign(data)
    ret_info = {
        'out_trade_no': out_trade_no,
        'appId': self._appid,
        'timeStamp': timestamp,
        'nonceStr': nonce_str,
        'package': package,
        'signType': 'RSA',
        'paySign': pay_sign,
    }

    return ret_info


def close(self, out_trade_no):
    """关闭订单
    https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_4_3.shtml
    :param self:
    :param out_trade_no: 商户订单号
    :return:
    """
    if out_trade_no:
        path = '/v3/pay/transactions/out-trade-no/%s/close' % out_trade_no
    else:
        raise Exception('商户订单号不存在.')
    params = {'mchid': self._mchid}
    ret_lst = self._build.request(path, method=RequestType.POST, data=params)
    if int(ret_lst[0]) == 204:
        ret_info = {
            'out_trade_no': out_trade_no,
            'code': "204",
            'message': '无数据'
        }
    else:
        ret_info = {
            'out_trade_no': out_trade_no,
        }
        ret_info.update(json.loads(ret_lst[1]))
    return ret_info


def query(self, out_trade_no):
    """查询订单
    :param self:
    :param out_trade_no:
    :return:
    """
    if out_trade_no:
        path = '/v3/pay/transactions/out-trade-no/%s' % out_trade_no + '?mchid=' + self._mchid
    else:
        raise Exception('请提交商户订单号.')
    ret_lst = self._build.request(path, method=RequestType.GET)
    ret_info = json.loads(ret_lst[1])
    return ret_info


def refund(self,
           out_trade_no,
           refund_money,
           total,
           reason=None,
           out_refund_no=None
           ):
    """申请退款
    :param self:
    :param out_trade_no:
    :param refund_money:
    :param total:
    :param reason:
    :param out_refund_no:
    :return:
    """
    if out_trade_no:
        params = {'out_trade_no': out_trade_no}
    else:
        raise Exception('没上传商户订单号.')
    if out_refund_no is None:
        out_refund_no = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    params.update({'out_refund_no': out_refund_no})
    if reason:
        params.update({'reason': reason})
    params.update({'notify_url': self._notify_url})
    if refund:
        params.update({'amount': {
            'refund': refund_money,
            'total': total,
            "currency": "CNY"
        }})
    else:
        raise Exception('没上传金额.')
    path = '/v3/refund/domestic/refunds'
    ret_lst = self._build.request(path, method=RequestType.POST, data=params)
    ret_info = json.loads(ret_lst[1])
    return ret_info


def query_refund(self, out_refund_no):
    """查询单笔退款
    :param self:
    :param out_refund_no:
    :return:
    """
    path = '/v3/refund/domestic/refunds/%s' % out_refund_no
    ret_lst = self._build.request(path)
    ret_info = json.loads(ret_lst[1])
    return ret_info


def trade_bill(self, bill_date, bill_type='ALL', tar_type='GZIP', sub_mchid=None):
    """申请交易账单
    :param self:
    :param bill_date:
    :param bill_type:
    :param tar_type:
    :param sub_mchid:
    :return:
    """
    path = '/v3/bill/tradebill?bill_date=%s&bill_type=%s&tar_type=%s' % (bill_date, bill_type, tar_type)
    if self._partner_mode and sub_mchid:
        path = '%s&sub_mchid=%s' % (path, sub_mchid)
    return self._build.request(path)


def fundflow_bill(self, bill_date, account_type='BASIC', tar_type='GZIP'):
    """申请资金账单
    :param self:
    :param bill_date:
    :param account_type:
    :param tar_type:
    :return:
    """
    path = '/v3/bill/fundflowbill?bill_date=%s&account_type=%s&tar_type=%s' % (bill_date, account_type, tar_type)
    return self._build.request(path)


def download_bill(self, url):
    """下载账单
    :param self:
    :param url:
    :return:
    """
    path = url[len(self._build._gate_way):] if url.startswith(self._build._gate_way) else url
    return self._build.request(path)
