# 云软算法 - 访问授权和数据授权

![title](https://raw.githubusercontent.com/yunsoft-design/image/LICENSE/ys_readme_title.png)

## 介绍

云软算法通过访问令牌访问授权,通过明文数据、签名数据、和加密数据对数据授权。</br>

### 安全认证流程

#### 请求方

1 请求方对提交数据（全部或部分）加密。</br>
2 请求方对提交数据（全部或部分）签名。</br>
3 请求方把访问令牌、加密数据、签名数据按每个接口的要求提交到服务端。</br>

#### 服务端

1 解析令牌，确保用户身份正确。</br>
2 验证签名，确保请求的确来源于约定的请求方。</br>
3 解密数据，确保数据传输正确完整，未被篡改。</br>

**根据每个接口的安全级别,对全部或部分数据可选择明文、密文、签名**

请扫下面微信公众号【倚云算法】交流,有问必答。</br>

![qrcode](https://raw.githubusercontent.com/yunsoft-design/image/LICENSE/ys_wechat_qrcode.jpg)

```python
"""
服务端接收数据使用示例
"""
from django.views.generic import View
from django.conf import settings
from cloud_soft.ys_interaction import FrontToBackend, BackendToFront
from django.db import models
from cloud_soft.ys_models import BaseAbsModel


class VisitInfo(BaseAbsModel):
    """
    日志信息模型
    """
    METHOD = (
        (1, '电脑'),
        (2, '手机'),
    )
    ip = models.CharField(max_length=20, verbose_name='请求ip')
    method = models.SmallIntegerField(choices=METHOD, default=1, verbose_name='请求方式')
    user_info = models.ForeignKey(to='UserInfo', null=True, on_delete=models.CASCADE, related_name='user_info_find_visit_info', verbose_name='用户id')
    inter_code = models.CharField(max_length=20, verbose_name='请求接口编号')
    params = models.TextField(null=True, verbose_name='上传参数')
    result = models.TextField(null=True, verbose_name='返回参数')
    expand = models.IntegerField(default=0, verbose_name='消耗时间')

    class Meta:
        db_table = 'bas_visit_info'
        app_label = 'nucleus'


class VisitFailure(BaseAbsModel):
    """
    日志错误模型
    """
    visit_info = models.ForeignKey(to=VisitInfo, on_delete=models.CASCADE, related_name='visit_info_find_visit_failure', verbose_name='日志主表')
    failure = models.TextField(null=True, verbose_name='错误信息')
    expand = models.IntegerField(default=0, verbose_name='消耗时间')

    class Meta:
        db_table = 'bas_visit_failure'
        app_label = 'nucleus'

class Cryption01(View):
    """
    签名测试
    """

    @classmethod
    def get(cls, request):
        """
        @api {GET} /bases/Cryption01/ 01-031 加密
        @apiVersion 1.0.0
        @apiName get_bases_cryption01
        @apiGroup 1BaseGroup
        @apiDescription <span style="color:#E62F28;font-size:18px;font-weight:bold">功能描述</span></br>
        <div style="background-color:#000;color:#EB9732;padding:10px;border-radius:8px;font-family:Consolas;font-size:14px;padding:15px">
        数据签名测试</br>
        </div>
        @apiHeader {String} Content-Type =application/json
        @apiHeader {String} Accept =application/json
        @apiHeader {String} User-Agent =https://csoft139.com
        @apiHeader {String} Authorization 用户授权
        @apiParam {String} user_info_id 用户id
        @apiParam {String} app_info_id 应用appid
        @apiParamExample {json} body 参数样例
        {
            "user_info_id":"16539870723521560",
            "app_info_id":"16539870952345596"
        }
        @apiSuccessExample 执行成功
        HTTP 1.1/ 200K
        {
            "status": "1",
            "msg": "请求成功!",
            "data": {}

        }
        @apiUse FailResponse
        """
        inter_code = '01-031'
        receive = {}
        try:
            receive = FrontToBackend(
                request=request, # django请求
                inter_code=inter_code, # 接口编号
                visit_info=VisitInfo, # 访问信息表
                have_headers=True, # 是否检查请求头(请求头包含access_token和signature)
                secret_key=settings.SECRET_KEY,  # access_token密钥
                salt=settings.SALT, # access_token盐
                private_key='', # 私钥全路径
                method='GET', # 请求方式
                path='/bases/Sign01/' # 请求路径
            ).receive_params()
            ret_dct = {} # 执行业务函数
            BackendToFront.update_info(visit_info=receive['visit_info'], ret_dct=ret_dct)
            return BackendToFront.res_success(data=ret_dct)
        except Exception as e:
            if (len(receive)) > 0:
                BackendToFront.update_error(visit_info=receive['visit_info'], visit_failure=VisitFailure, e=e)
            return BackendToFront.res_error(error=e)
```
