# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 10:40
# @Author  : Alex.xu
# @File    : fff.py
# @Software: PyCharm
"""
import logging
import os
from base import file_utils
from app.config import ROOT_PATH
from idna import unicode
from xlsxwriter.workbook import *
from utils.base import py_loader
import types
import re
import xlrd
from xlutils.copy import copy
from utils.base import json_utils

S_CFG_ALL = "config.ini"
S_DATA_ABSPATH = ""
S_CFG_URL = "urlConfig.ini"
S_CFG_CASE = "tsetCase.xlsx"
S_FTYPE_HEADER_BODY = "txt"
T_FSUFFIX = ('xlsx', 'xls')
T_REQ_DIR = ('headers', 'body')  # 请求资源目录表
T_RUN_ENV = ('ANDROID', 'IOS')
T_INIT_CFG = ('ENV', 'ANDROID', 'IOS')
S_ENV_OPTION = 'platform'


def get_data_rpath(fpath):
    path = os.path.abspath(fpath)
    s_file_name = os.path.basename(fpath)
    s_file_rname = s_file_name.split('.')[0]  # 模块名(没有.py)
    s_dir_proot = ROOT_PATH  # 获取当前项目根目录
    # 拼接目录
    l_mid_path = path.split(ROOT_PATH)[1].split(s_file_name)[0].split(os.path.sep)  # 中间那部分的path
    s_dir_root = ""
    for i in l_mid_path:
        if i != '':
            s_dir_root = os.path.join(s_dir_root, i)

    s_dir_root = os.path.join(s_dir_proot, "testData", s_dir_root, s_file_rname)
    return s_dir_root


def create_cfg(fpath):
    '''
    创建测试用例数据配置文件
    :param fpath:用例模块完整路径
    :return:
    '''
    path = os.path.abspath(fpath)
    s_file_name = os.path.basename(fpath)
    s_file_rname = s_file_name.split('.')[0]  # 模块名(没有.py)

    s_dir_root = get_data_rpath(fpath)

    # 创建目录
    l_req_dir = [os.path.join(s_dir_root, i) for i in T_REQ_DIR]
    for i in l_req_dir:
        file_utils.mkdirs(i, tips=True)

    # s_dir_headers = os.path.join(s_dir_root, 'headers')
    # s_dir_params = os.path.join(s_dir_root, 'params')
    s_path_url = os.path.join(s_dir_root, S_CFG_URL)

    # 创建目录
    # file_utils.mkdirs(s_dir_headers, tips=True) #创建E:\PycharmProject\Service\test\testData\my_test_module\headers
    # file_utils.mkdirs(s_dir_params, tips=True)  #创建E:\PycharmProject\Service\test\testData\my_test_module\params

    # 创建文件url配置文件
    # file_utils.mkfile(s_path_url) #E:\PycharmProject\Service\test\testData\my_test_module\urlConfig.ini
    init_config(s_path_url)

    # 根据模块方法创建请求header，params文件
    l_method = py_loader.get_mname_list(path)
    # 创建excel文件
    create_case_data(s_dir_root, l_method)


def get_config_value(seletion, key):
    s_path_url = os.path.join(ROOT_PATH, S_CFG_ALL)
    config = file_utils.ReadConfig(s_path_url)
    path = config.get(seletion, key)
    path = unicode(path, "utf-8")
    return path


def get_case_file_path(paths, suffix=T_FSUFFIX):

    l_fpath = []
    for path in paths.split(','):
        if os.path.isfile(path) and os.path.splitext(path)[1].strip(".") in suffix:
            l_fpath.append(os.path.abspath(path))
        elif os.path.isdir(path):
            l_fpath += file_utils.listfile(path, suffixes=suffix)
        else:#raise 错误
            print "Path %s does not exist." % str(path)
            sys.exit(-1)

    return l_fpath


def init_key(d_key_value, d_data, resp):
    s_k_vs = d_data.get('key-value')
    if s_k_vs != '' and s_k_vs is not None:
        for s_k_v in s_k_vs.split('\n'):
            s_k_v = s_k_v.strip()
            m = re.match(r'([a-zA-Z\_][0-9a-zA-Z\_]*)[\s]*=[\s]*(\$\.[\S]*)', s_k_v)
            try:
                key = m.group(1)
                if d_key_value.get(key) is None:
                    s_jsonpath = m.group(2)
                    d_key_value[key] = s_jsonpath
                    s_value = json_utils.get_data_by_jsonpath(resp, s_jsonpath)
                    if s_value:
                        d_key_value[key] = s_value
                else:
                    logging.warnings("key {} existing".format(m.group(1)))
            except:
                logging.error("{} jsonpath不正确: {}".format(d_data.get('casename'),s_k_v))


def before(jpath_express, d_k_v):
    l_check_exp = []
    s_key = ""
    s_exp_value = ""
    s_params = ""
    if jpath_express is not None:  # 如果有检验字段
        try:
            for i in jpath_express.split('\n'):
                pass

            return l_check_exp
        except:
            pass
    return l_check_exp


def init_config(s_path_url, cover=False):
    if cover:
        open(s_path_url, 'w')
    else:
        config = file_utils.ReadConfig(s_path_url)
        for i in T_INIT_CFG:
            config.add_section(i)
        config.set(T_INIT_CFG[0], S_ENV_OPTION, T_INIT_CFG[1])  # 默认平台为android


def insert_request_path(fpath, req_name):
    '''
    在请求配置文件中插入请求名字
    :param fpath:
    :param req_name:
    :return:
    '''
    s_dir_root = get_data_rpath(fpath)
    s_path_url = os.path.join(s_dir_root, S_CFG_URL)
    config = file_utils.ReadConfig(s_path_url)

    for i in T_RUN_ENV:
        try:
            config.get(i, req_name)  # 如果有就不插入
        except:
            config.set(i, req_name, "")


def create_request_files(fpath, req_name):
    '''
    创建请求文件('headers', 'body')
    :param fpath:
    :param req_name:
    :return:
    '''
    s_dir_root = get_data_rpath(fpath)
    l_req_dir = [os.path.join(s_dir_root, i) for i in T_REQ_DIR]
    create_file_by_mname([req_name], l_req_dir)


def create_case_data(s_dir_root, l_method, cover=False):
    '''
    创建xlsx文件存放case, 每个@testcase为一个sheet
    :param s_dir_root: xlsx文件名
    :param l_method: 方法列表
    :param cover: 是否覆盖
    :return:
    '''
    fpath = os.path.join(s_dir_root, S_CFG_CASE)
    if not os.path.exists(fpath):
        workbook = Workbook(fpath)
        for s_sheet_name in l_method:
            workbook.add_worksheet(u"%s" % s_sheet_name)
    elif cover:
        os.remove(fpath)
        workbook = Workbook(fpath)
        for s_sheet_name in l_method:
            workbook.add_worksheet(u"%s" % s_sheet_name)
    elif os.path.exists(fpath):
        old_excel = xlrd.open_workbook(fpath)
        # 将操作文件对象拷贝，变成可写的workbook对象
        new_excel = copy(old_excel)
        b_is_read = True
        for i in l_method:
            try:
                new_excel.get_sheet(i)
            except:
                new_excel.add_sheet(i)
                b_is_read = False
        if not b_is_read:  # 如果sheet都存在就不创建
            try:
                new_excel.save(fpath)
            except IOError:
                print "请确认excel文件是否关闭！"


def get_req_path(fpath, req_name):
    '''
    获取配置文件的path
    :param fpath:
    :return:
    '''
    config = file_utils.ReadConfig(fpath)
    s_platform_name = config.get(T_INIT_CFG[0], S_ENV_OPTION)
    return config.get(s_platform_name, req_name)


def create_file_by_mname(l_method, l_path):
    '''
    创建根据文件名方法列表和目录列表创建文件
    :param l_method:
    :param l_path:
    :return:
    '''
    for i in l_path:
        for j in l_method:
            s_fpath = os.path.join(i, "%s.%s" % (j, S_FTYPE_HEADER_BODY))
            file_utils.mkfile(s_fpath)


def get_module_method_list(path, s_dir_proot, s_file_name, s_file_rname):
    '''
    根据模块路径加载模块所有方法
    :param path: 模块完整路径
    :param s_dir_proot: 项目根目录
    :param s_file_rame: 模块名(有后缀)
    :param s_file_rname: 模块名(没有后缀)
    :return: 模块所有方法list
    '''
    # 掉用上一层目录的包

    sys.path.append("..")
    # __import__()
    a = path.split(s_dir_proot)[1]
    b = a.split(s_file_name)[0]
    c = b.split(os.path.sep)
    d = [i for i in c if i != '']

    # 导入my_test_module.py模块
    s_import = "from %s import %s" % ('.'.join(d), s_file_rname)

    exec (s_import)  #

    # __import__(s_file_rname, fromlist=d)

    # 获取模块所有方法列表
    l_method_name = []
    exec ("d_module = %s.__dict__" % s_file_rname)  # 获取木块所有属性和方法
    for k, v in d_module.items():
        if type(v) == types.FunctionType:
            l_method_name.append(k)
    return l_method_name


def load_config_key_value(path=None):
    '''
    加载配置文件中的全局变量
    :param d_data:
    :return:
    '''
    if not path:
        path = os.path.join(ROOT_PATH, S_CFG_ALL)
    config = file_utils.ReadConfig(path)
    l_key_value = config.get_all_name_value()
    result = {}
    for i in l_key_value:
        result[i[0]] = i[1]
    return result


if __name__ == "__main__":
    s_k_v = "a=$.afff"

    s_k_v2 = "a=$afff()"
    m = re.match(r'([a-zA-Z\_][0-9a-zA-Z\_]*)[\s]*=[\s]*(\$\.[\S]*)', s_k_v)

    m2 = re.match(r'([a-zA-Z\_][0-9a-zA-Z\_]*)[\s]*=[\s]*\$([\S]*)\(([\S\s]*)\)', s_k_v2)

    print(m.group(1))
    print(m.group(2))
    # key = m.group(1)
    # print m.group(0), m.group(1), m.group(2)
    # print m2.group(0)
    # print 'var = ', m2.group(1)
    # print 'method_name = ', m2.group(2)
    # print ('params = ', m2.group(3))
"""
