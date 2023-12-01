from datetime import datetime

def get_time(format_str='%y-%m-%d-%H%M%S'):
    """获取系统的当前时间，格式为 `23-01-01-000000`"""
    a = datetime.now()
    return a.strftime(format_str)