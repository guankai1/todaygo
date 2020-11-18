# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 9:58
# @Author  : gexm
# @File    : time_utils.py
# @Software: PyCharm
import datetime
import time
from common.handleExcel import digit_utils
from common.handleExcel import coding
import types
def time2long(s_time, fmt="yyyy-mm-dd hh:mm:ss"):
    if type(s_time) == str:
        s_time = s_time.encode('utf-8')
    s_time = str(s_time)
    if (s_time.startswith('"') and s_time.endswith('"')) or (s_time.startswith("'") and s_time.endswith("'")):
        s_time = s_time[1:-1]
    try:
        if fmt.lower() == "yyyy-mm-dd hh:mm:ss":
            t = time.mktime(time.strptime(s_time, '%Y-%m-%d %H:%M:%S'))  # 1482286976.0
            return digit_utils.round(t, 0)
        elif fmt.lower() == r"yyyy/mm/dd hh:mm:ss":
            pass
    except:
        return s_time

def to_second(stime):
    '''
    2,2s=2s, 2m=2*60s, 2h=2*3600s
    :param stime:
    :return:
    '''
    try:
        if stime is None:
            return None
        elif stime.endswith('s') or stime.endswith('S'):
            return float(stime[:-1])
        elif stime.endswith('m') or stime.endswith('M'):
            return float(stime[:-1]) * 60
        elif stime.endswith('h') or stime.endswith('H'):
            return float(stime[:-1]) * 3600
        else:
            return float(stime)
    except:
        return None


def cur_datetime(format='%Y-%m-%d'):
    '''
    获取当前时间
    :param format:
    :return:
    '''
    return datetime.datetime.now().strftime(format)

def timestamp(type='s'):
    '''
    获取当前时间戳
    @:param type: s表示秒，ms表示毫秒
    :return:
    '''
    if type == 'ms':
        return str(int(time.time()*1000))
    else:
        return str(int(time.time()))


if __name__ == "__main__":
    # 2018-06-04 19:34:27
    timestring = '2016-12-21 10:22:56'
    print(time2long(timestring))

    # 2018/6/5 10:30:46
