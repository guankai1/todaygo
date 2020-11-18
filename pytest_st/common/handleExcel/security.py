# -*- coding: utf-8 -*-
# @Time    : 2018/4/16 14:55
# @Author  : gexm
# @File    : security.py
# @Software: PyCharm
import hashlib
# from app import com
import base64
import json
import logging

import requests
from utils import  configurator
from common.myException.exceptions import AesEncryptException, MyException, ParamLoadException


def GetStringMD5(content):
    '''
    获取MD5码
    :param str:
    :return:
    '''
    m = hashlib.md5()
    m.update(str(content))
    return m.hexdigest()

def create_sign(params, apikey):
    '''
    创建签名
    :param params:
    :param apikey:
    :return:
    '''
    params_original = sorted(params.iteritems(), key=lambda asd: asd[0])
    sign_params = ''
    for item in params_original:
        try:
            sign_params = sign_params + str(item[0]) + '=' + str(item[1]) + '&'
        except:
            sign_params = sign_params + str(item[0].encode('utf8')) + '=' + str(item[1].encode('utf8')) + '&'

    sign_original = sign_params + apikey
    sign = GetStringMD5(sign_original)
    return sign

def get_aes(msg):
    '''
    趣看android加密
    :param msg:
    :return:
    '''
    #手机端ip
    url = configurator.get_config_value('HOST', 'aes_phone_client_host')
    body = msg
    hds = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "qukan_android"}
    try:
        resp = requests.post(url, data=body, headers = hds, timeout=4)
    except:
        raise AesEncryptException(u"加密地址请求失败:"+url)
    else:
        RESP_BODY = resp.text
        if resp.status_code == 200:
            return RESP_BODY
        else:
            raise AesEncryptException(RESP_BODY)

def aes_encrypt(msg, dtu=1):
    '''
    趣看android加密
    :param msg:
    :param dtu:
    :return:
    '''
    #手机端ip
    try:
        if dtu is None:
            dtu = 1
        else:
            dtu = int(dtu[-1])
    except:
        dtu = 1

    try:
        from utils.base.redis_utils import d_redis_conn
        rs_aes = d_redis_conn.get('aes').get_redis()
        if isinstance(msg, dict):
            jsonp = json.dumps(msg)
        else:
            jsonp = json.dumps(json.loads(msg))

        if dtu == 200:
            encrypt = rs_aes.hget('encrypt', 'h5.' + str('ab28c644-bc00-4f41-b34a-5a0e4f7410d1') + '.' + str(jsonp))
        elif dtu >= 100 and dtu < 300:  # ios key
            encrypt = rs_aes.hget('encrypt', 'ios.' + str('ab28c644-bc00-4f41-b34a-5a0e4f7410d2') + '.' + str(jsonp))
        else:
            encrypt = rs_aes.hget('encrypt', 'android.' + str('ab28c644-bc00-4f41-b34a-5a0e4f7410d9') + '.' + str(jsonp))

        encodestr = base64.b64encode(str(encrypt))
        return encodestr
    except ValueError as e:
        logging.error('请检查json字符串格式是否正确:{}'.format(msg))
        logging.error(e, exc_info=True)
        raise ParamLoadException(msg)
    except Exception as ex:
        logging.error(ex, exc_info=True)
        raise AesEncryptException()


def laotie_oauth(msg, version=None, rule=None):
    '''
    OAuth2协议
    (老铁)热点段子加密encrypt
    :param msg:
    :param rule:
    :return:
    '''
    d_temp = json.loads(msg)
    '''
    客户端加密密钥: vOXosfJOw5nf5IWprufoSbl/YE1p4MpYADvWy914zE4=
    客户端加密版本: 2

    新版客户端加密密钥:ZmsU4tREJ9P/NbGQIN2OzUmOkAwaJE3Yycom1GhYZUI=
    新版客户端加密版本: 6
    '''
    auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjk2LCJuYW0iOiJsaXdlbndlbiIsImlhdCI6MTU1MTQzMTAxMSwiZXhwIjoxNTUxNDMyODExLCJyb3MiOjQsInBkcyI6WyJrZGQiXX0.AARiyL4BPpHKBPeH9icrrtB82cd2PDSiqrdwVkNLXwY'
    headers = {'Authorization': 'Bearer ' + auth_token}
    d_params = {
        "encode": "1",
        "direction": "ctos",
        "version": "6",
        "platform": "android",
        "key": "ZmsU4tREJ9P/NbGQIN2OzUmOkAwaJE3Yycom1GhYZUI=",
        "params": "cf262ba1-4e26-4f87-9579-244517a4c5bb",
        "plain": msg
    }

    url = 'https://p1.innotechx.com/v1/tool/encrypt_test'
    try:
        res = requests.post(url, json=d_params, headers=headers)
        d_res = json.loads(res.text)
        return d_res['data']['cipher']
    except ValueError as e:
        logging.error('请检查json字符串格式是否正确:{}'.format(msg))
        logging.error(e, exc_info=True)
        raise ParamLoadException(msg)
    except Exception as ex:
        logging.error(ex, exc_info=True)
        raise AesEncryptException()


def laotie_oauth2(msg, version=None, rule=None):
    '''
    OAuth2协议
    (老铁)热点段子解密encrypt
    :param msg:
    :param rule:
    :return:
    '''
    auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjk2LCJuYW0iOiJsaXdlbndlbiIsImlhdCI6MTU1MTQzMTAxMSwiZXhwIjoxNTUxNDMyODExLCJyb3MiOjQsInBkcyI6WyJrZGQiXX0.AARiyL4BPpHKBPeH9icrrtB82cd2PDSiqrdwVkNLXwY'
    headers = {'Authorization': 'Bearer ' + auth_token}
    d_params = {
        "encode": "1",
        "direction": "ctos",
        "version": "2",
        "platform": "android",
        "key": "c3RvY0tleUwpJXdqWCVybzZNYkQpOnVWJiVyUjF0R3I=",
        "params": "cf262ba1-4e26-4f87-9579-244517a4c5bb",
        "cipher": msg
    }

    url = 'https://p.innotechx.com/v1/tool/encrypt_test'
    try:
        response = requests.post(url, json=d_params, headers=headers)
    except ValueError as e:
        logging.error('请检查json字符串格式是否正确:{}'.format(msg))
        logging.error(e, exc_info=True)
        raise ParamLoadException(msg)
    except Exception as ex:
        logging.error(ex, exc_info=True)
        raise AesEncryptException()

    print(response.text)

def encrypt_temp():
    s = '''{"image":"[null,null,null]","url":"http://kdd-middle-frontend-k8s-tst.qutoutiao.net/#/feedback","msg":"yyyy","type":1,"token":"6a7eLnL8RJnnduGhu_DR2YPAjE_ZV1gBJzzvaBjmLbXUrWsLoyuWxkDjHhNtf08tco2kdVPyusWdDb6uPRiP0mn0cmaOfvGPIz7DTA","sign":"3774e4de76bd2f77d9e9d7b02e5e675d","dtu":200}'''
    d = json.loads(s)


if __name__ == "__main__":
    # s = r'''{"date":"20180322","message":"Success !","status":200,"city":"北京","count":632,"data":{"shidu":"34%","pm25":73,"pm10":91,"quality":"良","wendu":"5","ganmao":"极少数敏感人群应减少户外活动","yesterday":{"date":"21日星期三","sunrise":"06:19","high":"高温 11.0℃","low":"低温 1.0℃","sunset":"18:26","aqi":85,"fx":"南风","fl":"<3级","type":"多云","notice":"阴晴之间，谨防紫外线侵扰"},"forecast":[{"date":"22日星期四","sunrise":"06:17","high":"高温 17.0℃","low":"低温 1.0℃","sunset":"18:27","aqi":98,"fx":"西南风","fl":"<3级","type":"晴","notice":"愿你拥有比阳光明媚的心情"}]}}'''

    s = r'''{"image":"[null,null,null]","url":"http://kdd-middle-frontend-k8s-tst.qutoutiao.net/#/feedback","msg":"fff","type":1,"token":"32696uJJBJm9jAj5hQCenloveMxZ7RepIci2zqwBoTyZkRadFsVuHma5chcOVxuqOTWdkpemld1Z7CdkfbwVjKUJGFrlwYMwgxyskg","sign":"177ea34d8a43765902d001f9342a157c","dtu":200}'''
    print (laotie_oauth(s))
