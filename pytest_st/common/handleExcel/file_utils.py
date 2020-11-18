# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 10:54
# @Author  : gexm
# @File    : file_utils.py
# @Software: PyCharm
import json
import logging
import os
import configparser
import xlrd
from common.handleExcel import coding
from configparser import DuplicateSectionError
import sys
from common.handleExcel.str_utils import remove_host_http_prefix

s_err_info = "Create fail! [%s] already exists."
s_ok_info = "Create [%s] success."


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=None)

    # 为了区分大小写
    def optionxform(self, optionstr):
        return optionstr


class ReadConfig(object):
    def __init__(self, configfile_path):
        self.configfile_path = configfile_path
        # self.cf = ConfigParser.ConfigParser()
        self.cf = MyConfigParser()  # 为了区分大小写
        self.__read()

    def __read(self):
        if not os.path.exists(self.configfile_path):
            with open(self.configfile_path, "w+") as f:
                pass
        self.cf.read(self.configfile_path)

    def __write(self):
        with open(self.configfile_path, "w+") as f:
            self.cf.write(f)

    def set(self, section, option, value=None):
        self.cf.set(section, option, value)
        self.__write()

    def get(self, section, option, value=None):
        return self.cf.get(section, option, raw=False, vars=None)

    def get_all_name_value(self):
        '''
        Return a list of tuples with (name, value) for each option in all section
        :return:
        '''
        all = []
        for i in self.cf.sections():
            all += self.cf.items(i)
        return all

    def add_section(self, section):
        try:
            self.cf.add_section(section)
            self.__write()
        except DuplicateSectionError:
            pass

    def get_all_sections_key_value(self):
        '''
        返回一个{'section':[(option, values), ...], ...}
        :return:
        '''
        return {section: dict(self.cf.items(section)) for section in self.cf.sections()}

    def get_sections(self):
        return self.cf.sections()


def listfile(path, suffixes=None, l_fs=[]):
    '''
    获取目录下面所有文件名(不包括~开头的文件)
    :param path: 目标目录
    :param suffixes: 文件后缀类型
    :return:
    '''

    for i in os.listdir(path):
        fpath = os.path.join(path, i)
        if os.path.isfile(fpath) and not os.path.basename(fpath).startswith('~'):
            if suffixes is None:
                l_fs.append(fpath)
            else:
                if os.path.splitext(fpath)[1].strip(".") in suffixes:
                    l_fs.append(fpath)
        elif os.path.isdir(fpath):
            listfile(fpath, suffixes, l_fs)
    return l_fs


def mkdirs(s_dir_path, tips=False):
    '''
    创建文件目录
    :param s_dir_path:目录提示
    :param tips:是否提示创建成功
    :return:
    '''

    try:
        os.makedirs(s_dir_path)
        if tips:
            pass
            # print s_ok_info % s_dir_path
    # except WindowsError:  #windows
    #     print s_err_info % s_dir_path
    except OSError:
        pass
        # print s_err_info % s_dir_path


def mkfile(s_file_path, cover=False):
    '''
    创建新文件
    :param s_file_path: 文件path
    :param cover: 是否覆盖
    :return:
    '''
    if cover:
        open(s_file_path, 'w')
    else:
        if not os.path.exists(s_file_path):
            open(s_file_path, 'w')


def case_config_loader(fpath):
    '''
    读取testcase excel文件中config sheet中的配置文件
    :param fpath: testcase文件目录
    :return:
    '''
    path = os.path.abspath(fpath)
    myworkbook = xlrd.open_workbook(path)
    mysheets = myworkbook.sheets()
    SPLIT = '='
    result = {}
    for mysheet in mysheets:
        if mysheet.name.lower() != 'config':
            continue
        for r in mysheet.col(0):
            if r.value.find(SPLIT) == -1:
                continue
            k, v = r.value.split(SPLIT, 1)
            result[k.strip()] = v.strip()
    print (result)
    return result


def case_xlsx_loader(fpath, sheets=None, name=None, tags=None):
    '''
    excel数据加载
    过滤条件包括：
    1. 只运行指定的sheet
    2. 只运行指定的用例名字
    3. 只运行tags标签指定的用例
    4. 只运行execute列中值为1的用例
    :param fpath:
    :return:
    '''
    path = os.path.abspath(fpath)
    # s_dir_root = configurator.get_data_rpath(path)
    myworkbook = xlrd.open_workbook(path, on_demand=True)
    # mysheet = myworkbook.sheet_by_name(cname)

    # mysheet = myworkbook.sheet_by_index(0)
    mysheets = myworkbook.sheets()
    datas = []
    for mysheet in mysheets:
        # 配置文件不解析
        if mysheet.name.lower() == 'config':
            continue
        # 只运行excel中指定的sheet名字
        if sheets and mysheet.name.strip() not in sheets:
            continue
        i = 0
        data = []
        l_col_names = []
        while (True):
            try:
                l_data = mysheet.row_values(i)
                i += 1
                if i == 1:
                    l_col_names = l_data
                    continue
                if l_data == []:
                    break
                # 过滤名字
                if name:
                    if l_col_names.count('casename') >= 0:
                        casename = l_data[l_col_names.index('casename')]
                        if casename != name:
                            continue
                # 过滤执行状态
                if l_col_names.count('execute') >= 0:
                    # 可能会有异常，非字母格式的内容，直接跳过
                    status = int(l_data[l_col_names.index('execute')])
                    if status != 1:
                        continue
                # 过滤tag标签
                if tags:
                    if l_col_names.count('tag') >= 0:
                        case_tag = l_data[l_col_names.index('tag')]
                        case_tags = set([_.strip().lower() for _ in case_tag.split(',')])
                        if not case_tags.intersection(tags):
                            # 运行参数tags和用例case_tags没有交集
                            continue
                    else:
                        # 不含tag列过滤
                        continue
                # 缺少元素用''补
                c = len(l_col_names) - len(l_data)
                for _ in range(c):
                    l_data.append('')
                d_row_data = {k: v for k, v in zip(l_col_names, l_data)}
                d_row_data['sheet_name'] = mysheet.name
                d_row_data['full_name'] = '{}_{}'.format(mysheet.name, d_row_data['casename'])
                data.append(d_row_data)
            except:
                break
        datas.append(data)
    #print (coding.unicode2str(datas))
    return datas #coding.unicode2str(datas)


def get_pic_type():
    return {
        "FFD8FF": "JPEG",
        "89504E47": "PNG",
        "47494638": "GIF",
        "49492A00": "TIFF",
        "424D": "BMP"
    }


def asc2hex(ss):
    s_hex = ""
    for i in ss:
        # print '%#x'% ord(i)
        s_hex += hex(ord(i))[-2:]
    return s_hex


def get_datatype(data):
    with open("_temp_pic.type", 'wb') as f:
        f.write(data.encode("utf-8"))
    with open("_temp_pic.type", 'rb') as f:
        binfile = f
        tl = get_pic_type()
        ftype = 'unknown'
        for hcode in tl.keys():
            numOfBytes = len(hcode) / 2  # 需要读多少字节
            f_hcode = asc2hex(binfile.read((numOfBytes))).upper()
            binfile.seek(0)
            if f_hcode == hcode:
                ftype = tl[hcode]
                break

    os.remove("_temp_pic.type")
    return ftype


def update_path_seperator(path):
    '''
    按照路径默认分隔符来更新路径
    :param path:
    :return:
    '''
    ori_sep = '/'
    if os.path.sep == ori_sep:
        # unix类
        ori_sep = '\\'
    return path.replace(ori_sep, os.path.sep)


def get_file_root_name(path):
    '''
    获取文件名字，去掉扩展名
    输入xyz/abc.txt，返回abc
    :param path:
    :return:
    '''
    return os.path.splitext(os.path.basename(path))[0]


def load_host_mapping_file(mapping_file):
    '''
    读取host_mapping.json文件
    :param mapping_file: 文件名字
    :return: json数据
    '''
    result = {}
    if not os.path.exists(mapping_file):
        return result

    try:
        with open(mapping_file) as f:
            data = f.readlines()
            content = ''.join([_ for _ in data])
            json_content = json.loads(content)
            for k, v in json_content.items():
                host = remove_host_http_prefix(k)
                result[host] = v
    except Exception as e:
        logging.error("读取host_mapping.json失败")
    finally:
        return result


if __name__ == "__main__":

    #print(get_datatype("aaaaaaa"))
    # config = ReadConfig(r"E:\PycharmProject\test2\test\testData\app\justtemp\urlConfig.ini")
    # # print cfg.cf.items("ANDROID", 'aa')
    # config.add_section('Section233')
    # config.set("Section233", "", "")
    # config.write()

    # configfile_path = r"E:\PycharmProject\test2\test\testData\app\justtemp\urlConfig.ini"
    # with open(configfile_path) as f:
    #     print f.read()

    # print cfg.cf.get("ANDROID", 'aa')
    #case_config_loader('C:\\Users\\qqq\\Desktop\\notebook\\qtt-api-test\\qtt-api-test\\user\\liaowang_testcase_offline.xlsx')
    list_type=case_xlsx_loader('C:\\Users\\qqq\\PycharmProjects\\pytest_st\\todayGogogo\\testdata\\todaygo_testcase_offline.xlsx',sheets='服务相关',name=None,tags=None)
    print(type(list_type))
    print(list_type[0][0])
