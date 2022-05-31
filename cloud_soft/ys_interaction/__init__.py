#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 前后台交互类
创建    : 2022-05-29 8:29
更新    : 2022-05-29 8:29
编写    : 陈倚云
"""
import ast
import json
import re
import time
from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
from ..ys_exception import YsException
from ..ys_transition import YsTransition
from ..ys_crypto import YsCrypto


class BackendToFront:
    """
    返回数据到前端
    """

    @classmethod
    def res_success(cls, msg='请求成功!', status=200, data=''):
        """
        返回正确信息
        """
        response = HttpResponse(
            content=json.dumps({
                'status': 200,
                'msg': msg,
                'data': data
            }))
        response.status_code = status
        return response

    @classmethod
    def res_error(cls, msg='请求失败!', status=404, error=''):
        """
        返回错误信息
        """
        error_info = '' if len(str(error).strip()) == 0 else ast.literal_eval(str(error))
        response = HttpResponse(
            json.dumps({
                'status': 404,
                'msg': msg,
                'error_info': error_info
            }))
        response.status_code = status
        return response

    @staticmethod
    def update_info(visit_info, ret_dct):
        """
        :param visit_info:访问信息
        :param ret_dct: 返回信息
        :return:
        """
        if visit_info == 0:
            return 0
        visit_info.result = ret_dct
        visit_info.expand = int(time.time() - int(visit_info.id/10000000))
        visit_info.save()

    @staticmethod
    def update_error(visit_info, visit_failure, e):
        """
        :param visit_info:访问信息
        :param visit_failure: 访问错误model
        :param e: 返回信息
        :return:
        """
        if visit_info == 0:
            return 0
        expand = int(time.time() - int(visit_info.id/10000000))
        visit_failure.objects.create(visit_info_id=visit_info.id, failure=str(e), expand=expand)


class FrontToBackend(object):
    """
    接收前端传来的数据
    """

    def __init__(self, request, inter_code, visit_info, private_key=None, method=None, path=None):
        """
        :param request: 前端请求
        :param inter_code: 接口编号
        :param visit_info: 访问模型
        """
        self._request = request
        self._inter_code = inter_code
        self._visit_info = visit_info
        self._private_key = private_key
        self._method = method
        self._path = path

    def check_mobile(self):
        """
        demo :
            @app.route('/m')
            def is_from_mobile():
                if checkMobile(request):
                    return 'mobile'
                else:
                    return 'pc'
        """
        user_agent = self._request.headers['User-Agent']
        # userAgent = env.get('HTTP_USER_AGENT')

        long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
        long_matches = re.compile(long_matches, re.IGNORECASE)
        short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(' \
                        r'mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(' \
                        r'aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(' \
                        r'o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(' \
                        r'ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(' \
                        r'18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(' \
                        r'\-|2|g)|yas\-|your|zeto|zte\- '
        short_matches = re.compile(short_matches, re.IGNORECASE)

        if long_matches.search(user_agent):
            return 2
        u_agent = user_agent[0:4]
        if short_matches.search(u_agent):
            return 2
        return 1

    def get_ip(self):
        """
        根据请示获取ip
        :return:
        """
        x_forwarded_for = self._request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        else:
            ip = self._request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
        return ip

    def verify_sign(self, headers, body):
        """
        验签
        :param headers:
        :param body:
        :return:
        """
        if self._private_key is not None:
            signature = YsTransition.standard_str(headers.get('signature', None))
            sign_lst = signature[18:].split(',', 4)
            sign_info = {}
            for item in sign_lst:
                item_lst = item.split('=', 1)
                sign_info.update({item_lst[0]: item_lst[1]})
            signature = eval(sign_info['signature'])
            body = body if isinstance(body, str) else json.dumps(body) if body else ''
            sign_str = YsCrypto.get_sign_str(
                method=self._method,
                path=self._path,
                time_stamp=sign_info['timestamp'],
                nonce_str=sign_info['nonce_str'],
                body=body
            )
            verify = YsCrypto.verify_sign(signature, sign_str, self._private_key)
            return verify
        else:
            return True

    def receive_params(self):
        """
        接收前端参数
        """
        try:
            authorization = self._request.META.get('HTTP_AUTHORIZATION', None)
            header_params = {} if authorization is None or len(authorization) == 0 else json.loads(authorization)
        except Exception:
            raise YsException('E0001', 'authorization数据格式错误')
        access_token = header_params.get('access_token', None)
        user_info_id = header_params.get('user_info_id', None)
        if access_token is not None and user_info_id is not None:
            conn = get_redis_connection('cloud_soft_token')
            a_token = conn.get(user_info_id)
            if a_token is None or access_token != bytearray(a_token).decode():
                raise YsException('E0002', 'access_token访问令牌无效')
        try:
            # 1 生成请求字典
            url_params = {}
            if (self._request.method == 'GET' or self._request.method == 'POST') and len(self._request.GET) > 0:
                for key in self._request.GET:
                    if len(self._request.GET.get(key)) == 0:
                        body = json.loads(key)
                        if isinstance(body, str):
                            url_params.update(json.loads(body))
                        else:
                            url_params.update(body)
                    else:
                        url_params.update({key: self._request.GET.get(key)})
            body_params = {}
            if len(self._request.body) > 0:
                if isinstance(self._request.body, bytes):
                    body = json.loads(self._request.body)
                    body = json.loads(body)
                    body_params.update(body)
                elif isinstance(self._request.body, str):
                    body = json.loads(self._request.body)
                    if isinstance(body, str):
                        body_params.update(json.loads(body))
                    else:
                        body_params.update(body)
            # 验签
            if not self.verify_sign(header_params, body_params):
                raise YsException('E0003', '验签失败')
            # 2 保存请求信息
            params = {**header_params, **url_params, **body_params}
            user_info_id = None if params.get('user_info_id', None) is None or len(str(params['user_info_id']).strip()) == 0 else int(params['user_info_id'])
            is_mobile = self.check_mobile()
            ip = self.get_ip()
            visit_info = self._visit_info.objects.create(ip=ip, method=is_mobile, inter_code=self._inter_code, user_info_id=user_info_id, params=params)
            print(self._inter_code, params)
            return {
                'params': params,
                'visit_info': visit_info
            }
        except Exception as e:
            raise YsException('E0001', '上传参数错误', e)
