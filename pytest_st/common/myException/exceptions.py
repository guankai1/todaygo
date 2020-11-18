# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 17:04
# @Author  : Alex.xu
# @File    : exceptions.py
# @Software: PyCharm

class MyException(Exception):
    def get_message(self):
        l_args = [str(i) for i in self.args]
        return self.message.encode('utf8') + ''.join(l_args)


class KeyNotExistException(MyException):
    "Base exception used by this module."
    message = u"变量${}不存在:"

class ParamLoadException(MyException):
    "Base exception used by this module."
    message = u"参数加载失败"


class AesEncryptException(MyException):
    "Base exception used by this module."
    message = u"AES加密失败"


class HttpRequestsException(MyException):
    "请求异常"
    message = u"请求失败"


class CaculateException(MyException):
    "计算失败"
    message = u"计算失败"


class QueueEmptyException(Exception):
    "Exception raised by Queue.get(block=0)/get_nowait()."
    message = u"计算失败"


class DBconnException(Exception):
    "Exception raised by Queue.get(block=0)/get_nowait()."
    message = u"MySql数据库连接失败"


class DBqueryException(Exception):
    "Exception raised by Queue.get(block=0)/get_nowait()."
    message = u"MySql数据库查询失败"


class ExpressException(Exception):
    "Exception raised by Queue.get(block=0)/get_nowait()."
    message = u"表达式格式错误"


class WksNotFoundException(Exception):
    def get_message(self):
        l_args = [str(i) for i in self.args]
        return self.message.encode('utf8') + ''.join(l_args)
# try:
#     raise AesEncryptException("hahah", "aaaa ")
# except Exception as ex:
#     print ex.get_message()
# class HTTPWarning(Warning):
#     "Base warning used by this module."
#     pass
#
#
# class PoolError(HTTPError):
#     "Base exception for errors caused within a pool."
#     def __init__(self, pool, message):
#         self.pool = pool
#         HTTPError.__init__(self, "%s: %s" % (pool, message))
#
#     def __reduce__(self):
#         # For pickling purposes.
#         return self.__class__, (None, None)


