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
from django.db import models
from cloud_soft.ys_models import BaseAbsModel
from cloud_soft.ys_interaction import FrontToBackend


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

receive = FrontToBackend(
    request='',  # django视图接收的request
    inter_code='',  # 接口编号
    visit_info='',  # 访问信息表
    have_headers=True,  # 是否验证请求头
    secret_key='',  # token密钥
    salt='',  # token盐 
    private_key='',  # 私钥全路径及文件名
    method='GET',  # 请求方式
    path='/bases/Sign01/'  # 请求路径
).receive_params()
```
