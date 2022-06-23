# 日期类

```python
"""
日期类
"""
from cloud_soft.ys_date import YsDate

# 01 获取时间戳
timestamp = YsDate.get_timestamp()
# 02 时间戳转时间
change_time = YsDate.timestamp_to_time(timestamp=timestamp)
# 03 确定某一年是否是润年
is_leap_year = YsDate.is_leap_year(year=2010)
# 04 计算某个日期到公元元年一月一日的总天数
total = YsDate.get_total_days(str_date='2021-01-01')
# 05 生成微信日期格式
wechat_time = YsDate.wechat_time(time_str='', fmt='%Y-%m-%d %H:%M:%S')
```
