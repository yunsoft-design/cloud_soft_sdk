# 云软算法-Django框架组件 API Python SDK

![title](https://raw.githubusercontent.com/yunsoft-design/image/LICENSE/ys_readme_title.png)

## 介绍

云软算法Django工程SDK1.0版 欢迎组件开发者共同完善，请扫下面微信公众号【倚云算法】交流,有问必答。

![qrcode](https://raw.githubusercontent.com/yunsoft-design/image/LICENSE/ys_wechat_qrcode.jpg)

## 目标
帮助更多程序员从纯技术中解脱出来，把更多的时间用于深入分析业务逻辑

## 适用对象
有django基础，但开发大型项目经验不足的程序员

## 安装
```
$ python.exe -m pip install --upgrade pip
$ pip install https://codeload.github.com/yunsoft-design/cloud_soft_sdk/zip/refs/heads/master
```

## 使用方法

[01 转换类](https://github.com/yunsoft-design/cloud_soft_sdk/blob/master/cloud_soft/ys_transition/transition.md)  
[02 自定义异常类](https://github.com/yunsoft-design/cloud_soft_sdk/blob/master/cloud_soft/ys_exception/exception.md)  
[03 装饰函数](https://github.com/yunsoft-design/cloud_soft_sdk/blob/master/cloud_soft/ys_decorate/decorate.md)  
[03 日期类](https://github.com/yunsoft-design/cloud_soft_sdk/blob/master/cloud_soft/ys_date/date.md)  
    
### 01 前后台交互类使用指南

```python
"""
    说明：主要用于接收前端数据和返回后端数据,可同时支持明码数据、签名数据和加密数据。考虑大数据分析用户请求,把接收数据,返回数据保存在VisitInfo模型中,把报错信息保存在VisitFailure模型里
        1 接收前端数据：可同时接收header、ajax和json数据,并进行组合解析
        2 返回后端数据：可同时返回header、json数据

"""
from django.views.generic import View
from django.db import models
from cloud_soft.ys_models import BaseAbsModel
from cloud_soft.ys_interaction import FrontToBackend, BackendToFront


class UserInfo(BaseAbsModel):
    """
    用户信息模型
    """
    real_name = models.CharField(max_length=50, null=True, verbose_name='姓名')
    mobile = models.CharField(max_length=20, unique=True, verbose_name='手机')

    class Meta:
        app_label = 'nucleus'
        db_table = 'bas_user_info'
        verbose_name = '用户信息模型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.real_name


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
    user_info = models.ForeignKey(to=UserInfo, null=True, on_delete=models.CASCADE, related_name='user_info_find_visit_info', verbose_name='用户id')
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


class Login01(View):
    """
    前后台交互
    """

    @classmethod
    def get(cls, request):
        """
        前后台交互请求
        """
        inter_code = '01-011'  # 接口编号
        # direct = '登录注册 ● 发送验证码'
        receive = FrontToBackend(request=request, inter_code=inter_code, visit_info=VisitInfo).receive_params()
        try:
            ret_dct = "def get(inter_code,direct,'接口名')"  # 执行函数,返回字典
            BackendToFront.update_info(visit_info=receive['visit_info'], ret_dct=ret_dct)
            return BackendToFront.res_success(data=ret_dct)
        except Exception as e:
            BackendToFront.update_error(visit_info=receive['visit_info'], visit_failure=VisitFailure, e=e)
            return BackendToFront.res_error(error=e)

```

### 02 日期类使用

```python
"""
    说明：针对日期处理的相关方法,不断丰富中...
"""
from cloud_soft.ys_date import YsDate

# 1 生成时间戳
timestamp = YsDate.get_timestamp()

# 2 时间戳转换成时间
ys_time = YsDate.timestamp_to_time('16536225145117')

# 3 确定某年度是否是闰年
is_leap = YsDate.is_leap_year(2010)

# 4 计算某个日期到公元元年一月一日的总天数
days = YsDate.get_total_days('2021-01-01')

# 5 格式化微信日期
wechat_time = YsDate.wechat_time('2022-05-06 11:10:01', '%Y-%m-%d %H:%M:%S')
```

### 03 自定义异常使用

```python
"""
    说明：所有异常返回错误编码、错误路径、错误信息和报错后跳转页面。
"""
from cloud_soft.ys_exception import YsException

try:
    pass
except Exception as e:
    YsException(
        errcode='E0001',  # 错误编码
        direct='小程序/发送消息',  # 错误路径
        errmsg=e,  # 错误信息
        errurl='www.csoft139.cn'  # 错误后跳转到的页面,
    )
```

### 04 obs服务类使用

```python
"""
    说明：华为obs服务,用于存储图片、语音、视频及其它文件。华为obs服务支持动态链接和链接有效期，可避免反复刷新
"""
from cloud_soft.ys_observer import YsObserver

client = YsObserver(
    access_key='',
    secret_access_key='',
    server_url='',
    bucket_name=''
)

# 1 obs文件名转全链接
file_url = client.get_obs_url(
    object_name=''  # obs文件名
)

# 2 根据图片url,下载图片并上传到为OBS
object_name2 = client.url_upload(
    url=''  # 图片url
)

# 3 直接上传文件
object_name3 = client.file_upload(
    file_path=''  # 文件全路径名
)

# 4 图片BASE64上传
object_name4 = client.base64_upload(
    content=b''
)

# 5 根据obs_name,下载文件
content = client.base64_down(
    object_name=''  # obs文件名
)
```

### 05 小程序类使用

```python
"""
    说明：主要用于微信小程序相关方法。
"""
from cloud_soft.ys_observer import YsObserver
from cloud_soft.ys_applet import YsApplet

# 只有生成带参二维码才需要传obs对象
observer = YsObserver(
    access_key='',
    secret_access_key='',
    server_url='',
    bucket_name=''
)
client = YsApplet(
    appid='',
    app_secret='',
    redis_alias='',
    observer=observer  # 只有需要生成带参二维码才需要此参数
)

# 1 解密用户信息
user_info = client.get_login_info(
    js_code=''
)

# 2 获取访问令牌
access_token = client.get_access_token()

# 3 解密小程序加密信息
decrpt = client.decrypted_unionid(
    session_key='',
    encrypted_data='',
    iv=''
)

# 4 生成带参二维码
# 4.1 生成A类带参二维码
qr_url_a = client.qrcode.create_qrcode_a(
    path='src/pages/mine/login?type=join&org_id=1'  # 小程序路径(包括参数)
)
# 4.2 生成B类带参二维码
qr_url_b = client.qrcode.create_qrcode_b(
    path='',  # 小程序路径(包括参数)
    scene=''  # 场景值
)
# 4.3 生成C类带参二维码
qr_url_c = client.qrcode.create_qrcode_c(
    path=''  # 小程序路径(包括参数)
)

# 5 发送通知 
# 根据不同的消息自定义通知
msg_info = client.nogice.send_user_request_msg(
    openid='',
    real_name='',
    post_name=''
)
```

### 06 字符串处理类使用

```python
"""
    说明：用于字符串相关处理，完善中...
"""
from cloud_soft.ys_character import YsCharacter

# 1 获取汉字首拼
spell_first = YsCharacter.get_spell_first(
    chn_str=''  # 中文字符串
)

# 2 判断字符串是否全是中文字符
is_chinese = YsCharacter.str_is_all_chinese(
    in_str=''  # 字符串
)

# 3 判断字符串是否包含中文
is_containts_chn = YsCharacter.str_contain_chinese(
    in_str=''  # 字符串
)

# 4 提取字符串中的中文字符
str_chn = YsCharacter.get_str_chn(
    in_str=''  # 字符串
)

# 5 获取字符类型
"""
1 中文
2 英文
3 英文标点
4 中文标点
5 数字
"""
str_style = YsCharacter.get_chr_style(
    charactor=''  # 字符
)
```

### 07 装饰函数使用

```python
"""
    说明：装饰函数，目前支持限制接口单时间内的访问次数,如果单位时间内访问次数过多,可限制访问,也可直接从redis缓存中获取相同数据。
"""
from django.views.generic import View
from cloud_soft.ys_decorate import rate_limit


@rate_limit(('06-03', 30))
class Test(View):
    """
    测试接口
    """

    @classmethod
    @rate_limit('01-001', 5)
    def get(cls):
        """
        请求
        """
        return ''
```

### 08 正则验证使用

```python
"""
    说明：正则表达式在python中的应用,完善中...
"""
from cloud_soft.ys_regular import YsRegular

# 1 验证手机号
is_mobile = YsRegular.mobile_is_valid('17856569985')

# 2 验证身份证
is_cert = YsRegular.cert_is_valid('988774164755584747')
```

### 09 访问令牌使用指南

```python
"""
    说明：用于生成token和解析token
"""
from cloud_soft.ys_token import YsToken

client = YsToken(
    secret_key='',  # 密钥
    salt=''  # 盐
)
token = client.create_token(info={
    'user_info_id': 1,
    'unicode': 'ADFDSAFDAS'
})
info = client.decode_token(token=token)
```

### 10 转换类使用指南

```python
"""
    说明：用于类型转换，完善中...
"""
from cloud_soft.ys_transition import YsTransition

# 1 字符串转字典
dct_obj = YsTransition.str_to_dict('{"name":"yunsoft"}')

# 2 unicode转码
decode_str = YsTransition.unicode_decode(
    uni_str=''  # unicode编码字符串
)

# 3 十进制转62进制
to62 = YsTransition.dec_to_sixty_two(456)

# 4 62进制转十进制
to10 = YsTransition.sixty_two_to_dec(to62)
```

### 11 短信验证使用指南

```python
"""
    说明：用于发送华为短信及短信验证
"""
from cloud_soft.ys_sms import YsSms

client = YsSms(
    sms_url='',  # 华为SMS接入地址(在控制台"应用管理"页面获取)+接口访问URI
    appkey='',  # 华为云appkey
    app_secret='',  # 华为云app_secret
    sender='',  # 国内短信签名通道号或国际/港澳台短信通道号
    template_id='',  # 华为短信模板id
    redis_alias=''  # redis别名,用于存储验证码
)

# 1 发送短信
result1 = client.send(
    receiver='17856998745'
)

# 2 验证验证码
result2 = client.verify_sms(
    receiver='17856998745',
    sms_code='342981'
)
```

### 12 经纬度转地址使用指南

```python
"""
    说明：用于高德地图中经纬度转详细地址
"""
from cloud_soft.ys_location import YsLocation

client = YsLocation(
    appkey=''  # 高德地图appkey
)
address = client.get(
    longitude=321.321,  # 经度
    latitude=432.534  # 纬度
)
```

### 13 华为隐私电话使用指南

```python
"""
    说明：用于华为隐私电话
"""
from cloud_soft.ys_private_tel import YsPrivateTel

client = YsPrivateTel(
    appkey='',  # 华为隐私电话appkey
    host='',  # 华为隐私电话服务器IP
    ak='',  # 华为隐私电话ak
    sk=''  # 华为隐私电话sk
)

# 1 绑定隐私电话
info1 = client.bind(
    tel_a='',  # 主叫
    tel_b='',  # 被叫
    tel_x=''  # 中转号
)

# 2 解除绑定
info2 = client.unbind(
    tel_x='',  # 中转号
    sub_id=''  # 绑定id
)

# 获取录音文件地址
info3 = client.get_voice_url(
    tel_x='',  # 中转号
    sub_id=''  # 绑定id
)
```

### 14 微信公众号SDK使用指南

```python
"""
    说明：用于微信公众号相关接口
"""
from cloud_soft.ys_wechat import YsWechat

client = YsWechat(
    wechat_token='',  # 微信公众号里设置的token
    appid='',  # 微信公众号appid
    app_secret='',  # 微信公众号app_secret
    redis_alias=''  # redis别名,存储微信公众号access_token访问令牌
)

# 1 菜单管理
# 1.1 创建菜单 
result1 = client.menu.create_menu(
    menu_dct={}  # 菜单列表
)
# 1.2 删除菜单
result2 = client.menu.del_menu()
# 1.3 查询菜单
result3 = client.menu.sql_menu()

# 2 用户管理
# 2.1 查询当前微信公众号所有用户
result4 = client.user.get_lst(
    next_openid=''  # 下一个开始的openid,为空则从第一条开始查询
)
# 2.2 根据openid列表,查询用户详情
result5 = client.user.get_info(
    user_lst=[]  # openid列表
)
# 2.3 给用户备注
result6 = client.user.remark(
    remark_dct={}  # 标签信息
)

# 3 客服管理
# 3.1 查询客服列表
result7 = client.service.get_lst()
# 3.2 添加客服账号
result8 = client.service.add(
    kf_account='',  # 客服账号
    nickname=''  # 客服昵称
)
# 3.3 邀请客服绑定账号
result9 = client.service.bind(
    kf_account='',  # 客服账号
    invite_wx=''  # 邀请微信号
)
# 3.4 删除客服账号
result10 = client.service.del_account(
    kf_account=''  # 客服账号
)
# 3.5 转发消息到指定客服
result11 = client.service.invit(
    from_user='',  # 发送人openid
    to_user=''  # 接收人openid
)

# 4 消息回复
# 4.1 发送跳转到小程序的消息
result12 = client.reply.reply_miniprogrampage(
    openid='',  # 接收人微信openid
    url=''  # 小程序路径
)
# 4.2 微信消息转发到指定客服
result13 = client.reply.text(
    from_user='',  # 发送人openid
    to_user='',  # 接收人openid
    content=''  # 发送内容
)
# 4.3 回复图文消息
result14 = client.reply.article(
    from_user='',  # 发送人openid
    to_user='',  # 接收人openid
    articles=[]  # 图文消息列表
)
```

### 15 云软签名使用指南

```python
"""
    说明：用于数据签名验签和数据加密解密
"""
from cloud_soft.ys_crypto import YsCrypto

# 1 获取包含大小字字母数字在内的随机数,用于加密字符串
api_key = YsCrypto.get_key(16)

# 2 获取组织编号
org_serial = YsCrypto.get_app_number()

# 3 获取uuid
uuid = YsCrypto.build_nonce_str()

# 4 生成私钥
private_pem = YsCrypto.get_private_pem()

# 5 私钥转公钥
public_pem = YsCrypto.get_public_key(private_pem)

# 6 公钥加密
cipher_text = YsCrypto.encrypt(
    private_dir='',  # 私钥全路径
    clear_text=''  # 需加密数据
)

# 7 私钥解密
clear_text = YsCrypto.decrypt(
    private_dir='',  # 私钥全路径
    cipher_text=''  # 加密数据
)
```

### 16 微信支付使用指南

```python
"""
    说明：用于微信支付相关功能
"""
from cloud_soft.ys_payment import YsPayment
from cloud_soft.ys_payment.type import PayType

client = YsPayment(
    pay_type=PayType.JSAPI,  # 微信支付类型
    mchid='',  # 直连商户号
    key_dir='',  # 商户证书私钥路径
    cert_serial_no='',  # 商户证书序列号
    appid='',  # 应用appid
    apiv3_key='',  # 商户APIV3密钥
    notify_url=''  # 通知地址
)

# 1 下单
ret_info1 = client.place(
    description='',  # 支付描述
    openid='',  # 支付者 JSAPI需要提供,NAVIVE不能提供
    total=5  # 以分为单位
)

# 2 关闭订单
ret_info2 = client.close(
    out_trade_no=''  # 商户订单号
)

# 3 订单查询
ret_info3 = client.query(
    out_trade_no=''  # 商户订单号
)

# 4 申请退款
ret_info4 = client.refund(
    out_trade_no='',  # 商户订单号
    refund_money=3,  # 退款金额(分)
    total=5,  # 订单总金额(分)
    reason=''  # 退款原因
)

# 5 查询退款
ret_info6 = client.query_refund(
    out_refund_no=''  # 商户退款单号
)

# 6 支付回调接口
call_back = client.callback(
    request=''  # Django请求对象
)
```
