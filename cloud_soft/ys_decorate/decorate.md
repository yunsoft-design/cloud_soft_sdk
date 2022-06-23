# 装饰函数

```python
"""
装饰函数：限制访问次数,可以设置3-5秒内访问,直接返回第一次请求的数据,少于3秒连续访问,则返回错误提示,超过5秒访问,重新执行。
"""
import json
from django.views.generic import View
from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
from cloud_soft.ys_decorate import rate_limit


class LimitVisit(View):
    """
    限制访问次数
    """

    @classmethod
    @rate_limit('06-03', 30)
    def get(cls, request):
        """
        测试接口
        """
        try:
            conn = get_redis_connection('limit_count')
            if request.META.get('HTTP_X_FORWARDED_FOR', None):
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
            else:
                ip = request.META.get('REMOTE_ADDR')
            ret_dct = {
                "name": "Chengl139"
            }
            key_word = '06-03/' + ip
            conn.set(key_word, json.dumps(ret_dct), 30)
            return HttpResponse(msg='查询成功')
        except Exception as e:
            return HttpResponse('查询失败' + str(e))
```