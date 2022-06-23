# 自定义异常类

```python
"""
自定义异常类
"""
from cloud_soft.ys_exception import YsException


def demo(inter_code, params, direct):
    """
    自定义异常使用方法
    """
    if params is None:
        raise YsException(inter_code, direct, '传入参数失败')
    try:
        pass
    except Exception as e:
        raise YsException(inter_code, direct, e)
```
