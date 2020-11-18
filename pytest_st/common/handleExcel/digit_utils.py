# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 10:14
# @Author  : gexm
# @File    : digit_utils.py
# @Software: PyCharm
import logging
import random


def round(f, n):
    '''
    保留几位小数，并且不四舍五入
    :param f:
    :return:
    '''
    if n <= 0:
        return int(str(f).split('.')[0])
    if f < 0:
        index = n + 3
    else:
        index = n + 2
    return float(str(f)[0:index])

def my_float(i, j, k):
    '''
    :param i:原来的数
    :param j: 左移多少位(填负数就是右移)
    :param k: 保留小数点后的多少位
    :return: 返回一个float类型的string
    '''
    a = float(i)/(10**j)
    s = str(a)
    all = s.split('.')

    if len(all) == 1:
        right = ""
    else:
        left, right = all[0], all[1]
    if k == 0:
        return left
    elif k < 0:
        raise Exception("k <0!")
    elif k > len(right):
        res = left + '.'+right+(k-len(right))*'0'
    else:
        res = left + '.' + right[0:k]
    return res

def get_random(n=None, pre=None):
    '''
    返回一个随机数
    :param n:n位随机数
    :param pre:
    :return:
    '''
    __pre = str(random.choice(range(1, 10)))
    __getran = lambda x: ''.join(str(random.choice(range(10))) for _ in range(x))
    if n is None:
        #返回1~11位随机数
        return __pre + __getran(10)
    else:
        if pre is None:
            return __pre + __getran(n-1) #返回n位随机数
        else:
            #返回以pre开头的随机数
            n1 = n-len(str(pre))
            if n1 < 1:
                return str(pre)
            else:
                return str(pre) + __getran(n1)


def phone(prefix=None):
    '''
    随机生成手机号
    :param prefix手机号前缀，比如137等
    :return:
    '''
    phone_len = 11
    if not prefix:
        prefix = ['13', '15', '16', '17', '18', '19'][random.randint(0, 5)]
    phone_len -= len(prefix)
    _ = str(random.randint(0, pow(10, phone_len) - 1))
    return prefix + '0' * (phone_len - len(_)) + _

if __name__ == "__main__":
    for i in range(100):
        logging.info(get_random(10))
