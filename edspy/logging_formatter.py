# 使用指定时区，不要当地时区
# 自定义 Formatter，指定时区（例如东八区）
import logging
from datetime import datetime, timezone, timedelta

class ChinaTimezoneFormatter(logging.Formatter):
    """中国时区 (UTC+8) 的日志时间格式化类"""
    def __init__(self, fmt=None, datefmt=None):
        self.china_tz = timezone(timedelta(hours=8))  # 固定东八区
        super().__init__(fmt=fmt, datefmt=datefmt)

    def formatTime(self, record, datefmt=None):
        # 将时间戳转换为东八区时间
        dt = datetime.fromtimestamp(record.created, tz=self.china_tz)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()
            
class TimezoneFormatter(logging.Formatter):
    def __init__(self, tz_offset=8, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tz = timezone(timedelta(hours=tz_offset))  # 设置时区

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.tz)
        return dt.strftime(datefmt) if datefmt else dt.isoformat()
