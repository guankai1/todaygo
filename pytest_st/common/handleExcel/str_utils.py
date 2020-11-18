# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 10:50
# @Author  : gexm
# @File    : str_utils.py
# @Software: PyCharm

import collections
import re
import types
import os
#from app.config import D_KEY_VALUE
from common.myException.exceptions import MyException
from common.handleExcel import time_utils
from common.handleExcel.data_structure import Queue

D_KEY_VALUE = {}
T_SEP = (':', '\t', ' ')
D_SEP = {'colon': ':', 't': '\t'}
D_BRACKETS = {'{': '}', '[': ']', '(': ')'}
D_NULL = {'null': None, 'NULL': None, 'Null': None}

class ContainsHelper(object):
    '''用来判断包含关系的'''
    def __init__(self, li):
        try:
            self.li = eval(li)
        except:
            self.li = li

    def __contains__(self, y):
        if (y.startswith("'") and y.endswith("'")) or (y.startswith('"') and y.endswith('"')):
            y = eval(y)
        if self.li.__contains__(y):
            return True
        else:
            try:
                return self.li.__contains__(int(y))
            except ValueError:
                return False


class Stack():
    def __init__(self):
        self.stack = []
        self.top = -1

    def push(self, x):
        self.stack.append(x)
        self.top = self.top + 1

    def pop(self):
        ''''''
        if self.is_empty():
            raise Exception("stack is empty")
        else:
            self.top = self.top - 1
            self.stack.pop()

    def is_empty(self):
        return self.top == -1

    def peek(self):
        '''
        :return:栈顶元素
        '''
        if self.stack is not []:
            return self.stack[self.top]
        else:
            return None


class Bracket():
    @classmethod
    def is_right_bracket(self, ch, brackets):
        '''
        判断是否为右括号
        :return: boolean
        '''

        l_right_brackets = [D_BRACKETS.get(i) for i in brackets]

        if ch in l_right_brackets:
            return True
        else:
            return False

    @classmethod
    def is_left_bracket(self, ch, brackets):
        '''
        判断是否为左括号
        :return: boolean
        '''
        # if ch == '(' or ch == '[' or ch == '{':
        if ch in brackets:
            return True
        else:
            return False

    @classmethod
    def is_peek(self, peek, c, brackets=('{',)):
        '''
        栈顶元素和右括号c是否匹配
        :param peek: 栈顶元素
        :param c:待匹配的字符
        :return:
        '''
        # 把只有左括号的加上右括号 brackets = ['{', '[', '(', ')', ']', '}']
        brackets = [i for i in brackets] + [D_BRACKETS.get(i) for i in brackets]

        temp = 0
        for i in brackets[len(brackets) / 2:]:
            if c == i:
                if peek == brackets[temp]:  # 根据对称来相等
                    return True
            temp += 1
        return False


def substr(str, start, end):
    return str[str.index(start) + len(start):str.index(end, str.index(start))]


def getPeek(strs, brackets=('(', '[', '{')):
    '''
    返回字符串指定括号匹配内容
    :param strs: 待匹配的字符串
    :param brackets: 匹配括号类型
    :return:
    '''
    s = Stack()
    temp = False
    start = 0
    for index, c in enumerate(strs):
        if Bracket.is_left_bracket(c, brackets):
            if temp is False:
                start = index
            temp = True
            s.push(c)
        elif Bracket.is_right_bracket(c, brackets):
            if s.is_empty():
                raise Exception("peek fail!")
            elif Bracket.is_peek(s.peek(), brackets) is not None:
                s.pop()
        if temp is True:  #
            if s.is_empty():
                return strs[start:index + 1]


def my_split(flag, s, tag='${', brackets=('(', '[', '{')):
    '''
    分割字符串,不分割${}里面的
    :param flag: 根据什么字符分割
    :param s: 要分割的字符串
    :return:
    '''
    data = s.split(flag)
    a = []
    stack = Stack()
    temp = ''
    for d in data:
        if stack.is_empty():
            temp += d
        else:
            temp += d
        if tag in d or not stack.is_empty():
            # temp = ',' + d
            for c in d:
                if Bracket.is_left_bracket(c, brackets):
                    stack.push(c)
                elif Bracket.is_right_bracket(c, brackets):
                    if stack.is_empty():
                        raise Exception("peek fail!")
                    elif Bracket.is_peek(stack.peek(), c) is not None:
                        stack.pop()
            if stack.is_empty():
                a.append(temp)
                temp = ''
        else:
            a.append(d)
            temp = ''
    return a


def my_split2(l_sep, s, tag='${', brackets=('(', '[', '{'), max_split=-1):
    '''
    分割字符串,不分割${}里面的
    :param l_sep: 根据什么字符分割
    :param s: 要分割的字符串
    :return:
    '''
    n = 0
    for flag in l_sep:
        if flag not in s:
            continue
        n += 1
        data = s.split(flag, max_split)
        l_res = []
        stack = Stack()
        temp = ''
        for d in data:
            if stack.is_empty():
                temp = temp + d
            else:
                temp = temp + flag + d

            if tag in d or not stack.is_empty():
                # temp = ',' + d
                for c in d:
                    if Bracket.is_left_bracket(c, brackets):
                        stack.push(c)
                    elif Bracket.is_right_bracket(c, brackets):
                        if stack.is_empty():
                            raise Exception("%s peek fail." % d)
                        elif Bracket.is_peek(stack.peek(), c) is not None:
                            stack.pop()
                if stack.is_empty():
                    l_res.append(temp)
                    temp = ''
            else:
                l_res.append(d)
                temp = ''
        if len(l_res) > 1:
            return l_res, flag
        else:
            continue
    if n > 0:
        return l_res, flag
    else:   #为了兼容单表达式(函数(函数返回默认为空))执行
        return [s], '='


def split_sep_with_list(s, l_sep, maxsplit=None):
    '''
    返回第一个符合列表的分割，分隔符
    :param s:
    :param l_sep:
    :param maxsplit:
    :return:
    '''
    for i in l_sep:
        l_res = s.split(i, maxsplit)
        # if "$.mysql" in s:
        #     l_res = my_split(i, s)
        # else:
        #     l_res = s.split(i, maxsplit)

        if len(l_res) > 1:
            if len(l_res) > 2:
                return [i.join(l_res[:-1]), l_res[-1]], i
            else:
                return l_res, i
        else:
            continue
    return s, None


def str2map(strs, sep=':', isorder=True):
    ss = strs.split('\n')
    # 通过OrderedDict类创建的字典是有序的
    if isorder:
        dic = collections.OrderedDict()
    else:
        dic = {}
    for i, s in enumerate(ss):
        try:
            k, v = s.split(sep, 1)
        except:
            v += s
        else:
            pass
        dic[k] = v.strip()
    return dic


def str2map2(strs, sep=':', isorder=True):
    '''
    string转map
    :param strs:
    :param sep:
    :param isorder:
    :return:
    '''
    # ss = strs.split('\n')
    ss = my_split('\n', strs, '{')  # 以'\n'分割,{}内面的不分割
    ss = [i.replace('\n', '') for i in ss]
    # 通过OrderedDict类创建的字典是有序的
    if isorder:
        dic = collections.OrderedDict()
    else:
        dic = {}

    is_json = False  # 当前行是否是json多行复合形式
    for i, s in enumerate(ss):
        try:
            k, v = s.split(sep, 1)
        except:
            if is_json:  # 如果上一行是json多行复合形式，而出现异常就，代表上一行还没完
                v += s
            else:  # 说明不是因为复合json格式引起的错误
                if sep == "\t":  # 可能是空格和\t混淆了
                    try:
                        k, v = s.split(" ", 1)
                    except:  # 再出错就代表这一行只有key没有value,设置value默认为空
                        k, v = s, ''
                elif sep == " ":
                    try:
                        k, v = s.split("\t", 1)
                    except:  # 再出错就代表这一行只有key没有value,设置value默认为空
                        k, v = s, ''
        else:
            s_v = v.strip()
            if s_v.startswith("{") or s_v.startswith("["):
                is_json = True  # 当前行是json多行复合形式
            else:
                is_json = False
        #TODO :在这里加文件过滤的方法，如果v可以加载为一个文件就以文件形式返回出去,如果不能就返回原值
        v = v.strip()
        dic[k] = load_file(v)
    return dic


def __get_context_type(suffix):
    '''
    根据后缀返回文件context type
    :param suffix:
    :return:
    '''
    d_context_type = {'.jpg': 'image/jpg',
                      '.csv': 'text/csv',
                      '.txt': 'text/plain',
                      '.jpeg': 'image/jpeg',
                      '.gif': 'image/gif'}
    ct = d_context_type.get(suffix)
    if ct is None:
        raise Exception(u"后缀格式%s不支持." % suffix)
    return ct


def load_file(s_path):
    if os.path.isfile(s_path):
        #获取文件名
        fname = os.path.basename(s_path)
        fcontext_type = __get_context_type(os.path.splitext(os.path.basename(s_path))[1].lower())
        s_path = (fname, open(s_path, 'rb'), fcontext_type)
    return s_path

def get_separator(s_body):
    '''
    获取分隔符
    :param s_body:
    :return:
    '''
    d_sep_count = {}
    l_items = s_body.split('\n')
    for sep in T_SEP:
        for i in l_items:
            if not i.startswith("\\\\"):
                i = i.strip()
                n = len(i.split(sep, 1))
                if n == 2:
                    if not d_sep_count.get(sep):
                        d_sep_count[sep] = 1
                    else:
                        d_sep_count[sep] += 1

    t = sorted(d_sep_count.items(), key=lambda x: x[1], reverse=True)

    # 如果参数都为空
    if t == []:
        d_sep = {}
        for sep in T_SEP:
            d_sep[sep] = 0
            for i in l_items:
                if sep in i:
                    d_sep[sep] += 1
        t = sorted(d_sep.items(), key=lambda x: x[1], reverse=True)
    return t[0][0]



def check_fun_and_replace(json_str):
    re1 = re.compile(r'(\$[a-zA-Z\_][0-9a-zA-Z\_]*\()')
    res = re1.findall(json_str)
    if res != []:
        for i in res:
            k = i[2:-1].strip()
            v = '"%s"' % D_KEY_VALUE[k]  # 这里！
            json_str = json_str.replace(i, v)  # 用最新的value替换~~
    return json_str


def get_params(exp):
    res = re.findall(r'\((.*?)\)', exp)
    return [i.strip()[1:-1] for i in res[0].split(',')]


def get_params2(exp, d_k_v):
    '''
    str转成参数列表
    目前只支持str,int,float,bool
    :param exp:
    :return:
    '''
    # l_res1 = exp.split(',')
    if exp == "":
        return []
    l_res1 = my_split2(",", exp, tag='"')[0]
    res = []
    for i in l_res1:
        i = i.strip()
        if (i[0] == '"' and i[-1] == '"') or (i[0] == "'" and i[-1] == "'"):
            res.append(i[1:-1])
        elif i.isdigit():
            res.append(int(i))
        else:
            try:
                i = float(i)
            except:
                p = str2bool(i)

                # 判断是否为布尔型，如果是就返回bool，不是当作变量,返回他的变量值
                if isinstance(p, bool):
                    res.append(p)
                else:
                    res.append(d_k_v.get(p))
            else:
                res.append(i)
    return res


def get_params3(exp):
    '''
    提取函数请求小括号里面的值，按照逗号进行分隔
    :param exp:
    :return:
    '''
    res = re.findall(r'\((.*?)\)', exp)
    param = res[0]
    escape_count = 0
    match = 0
    result = []
    inx_begin = 0
    inx_end = -1
    for i in range(len(param)):
        item = param[i]

        # 转义字符的处理
        if escape_count:
            escape_count = 0
            continue
        elif item == '\\':
            escape_count = 1
            continue

        # 逗号的处理
        if item == ',' and not match:
            if inx_end != -1:
                # 字符串类型
                result.append(param[inx_begin:inx_end])
            else:
                result.append(param[inx_begin:i].strip())
            inx_begin = i + 1
            inx_end = -1
            continue

        # 引号的处理
        if item not in ["'", '"']:
            continue
        cur_match = ['', '"', "'"].index(item)
        if match:
            if cur_match != match:
                continue
            else:
                # 找到配对的字符串，重新开始计算
                inx_end = i
                match = 0
        else:
            match = cur_match
            inx_begin = i + 1

    if inx_end != -1:
        result.append(param[inx_begin:inx_end])
    else:
        result.append(param[inx_begin:len(param)].strip())
    return result


def variable_substitution(json_str, d_k_v, extra_quote=False):
    '''
    将字符串中的${name}替换为给定的值
    :param json_str:
    :param d_k_v:
    :param extra_quote: 是否需要额外的引号
    :return:
    '''

    re1 = re.compile(r'(\$\{[a-zA-Z\_][0-9a-zA-Z\_]*\})')
    res = re1.findall(json_str)
    if res != []:
        for i in res:
            k = i[2:-1].strip()
            value = d_k_v.get(k)
            if value==None:
                raise MyException('读取参数${{{}}}错误，值不存在'.format(k))
            reg_temp = "^[1-2]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
            res_temp = re.match(reg_temp, value)
            my_format = '{}'

            if res_temp is not None:
                pass  # 时间格式的就不加双引号
            elif is_str_inner(json_str, r"\$\[\{[\s\S]*(\$\{%s\})[\s\S]*\}\]" % k):  # 判断里面是否有里面是否有{ }:
                my_format = '"{}"'
            elif extra_quote:
                my_format = '"{}"'
            v = my_format.format(d_k_v[k])  # 这里！

            json_str = json_str.replace(i, v)  # 用最新的value替换~~
    return json_str


def aes_data(data, d_k_v):
    from utils.http import security
    # data = data.replace("\n", '')
    # re1 = re.compile(r'(\$\[.*\])')
    dtu = d_k_v.get('dtu')
    re1 = re.compile(r'(\$\[[\s\S]*\])')
    res = re1.findall(data)
    is_66 = False
    if data.startswith('qdata__66'):
        is_66 = True
        data = 'qdata' + data[9:]
    elif data.startswith('qdata_66'):
        is_66 = True
        data = 'qdata' + data[8:]
    #判断是否普通的aes加密
    if res != []:
        for i in res:
            before_data = i[2:-1].strip()  #
            if is_66:
                if not before_data.startswith('{'):
                    before_data = str2map2(before_data, sep=get_separator(before_data), isorder=False)
                s_after_data = security.laotie_oauth(before_data, dtu)
            else:
                # s_before_data = i[2:-1].strip().lower() #这里为啥要转小写？
                # s_after_data = security.get_aes(s_before_data)
                if not before_data.startswith('{'):
                    before_data = str2map2(before_data, sep=get_separator(before_data), isorder=False)
                s_after_data = security.aes_encrypt(before_data, dtu)
            data = data.replace(i, s_after_data)
    return data


def cut_str(text, lenth):
    '''
    字符串按指定长度等分
    :param text:
    :param lenth:
    :return:
    '''
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr


def pretty2str(obj, indent=' '):
    '''
    美化输出str
    兼容dict,list
    :param obj:
    :param indent: 分隔符
    :return:
    '''

    def _pretty(obj, indent):
        if isinstance(obj, (dict)):
            if obj == {}:  # 如果不加这个，空list就不会返回东西
                yield '{}'
            else:
                for i, tup in enumerate(obj.items()):
                    k, v = tup

                    # 如果是字符串则拼上""
                    if isinstance(k, basestring):
                        k = k.replace("\\", "\\\\")
                        k = '"%s"' % k
                    if isinstance(v, basestring):
                        v = v.replace("\\", "\\\\")
                        v = '"%s"' % v
                    if isinstance(k, types.UnicodeType):
                        k = k.encode('utf-8')
                    if isinstance(v, types.UnicodeType):
                        v = v.encode('utf-8')

                    # 如果是字典则递归
                    if isinstance(v, dict):
                        v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
                    if isinstance(v, list):
                        v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
                    # case,根据(k,v)对在哪个位置确定拼接什么

                    if isinstance(k, types.UnicodeType):
                        k = k.encode('utf-8')
                    if isinstance(v, types.UnicodeType):
                        v = v.encode('utf-8')

                    # 因为python和json里面的boolean值大小写不一样,统一转换成小写的
                    if v is True:
                        v = 'true'
                    elif v is False:
                        v = 'false'

                    if i == 0:  # 开头,拼左花括号
                        if len(obj) == 1:
                            yield '{%s: %s}' % (k, v)
                        else:
                            yield '{%s: %s,\n' % (k, v)
                    elif i == len(obj) - 1:  # 结尾,拼右花括号
                        yield '%s%s: %s}' % (indent, k, v)
                    else:
                        yield '%s%s: %s,\n' % (indent, k, v)
        elif isinstance(obj, (list)):
            if obj == []:  # 如果不加这个，空list就不会返回东西
                yield '[]'
            else:
                for i, list_node in enumerate(obj):
                    if isinstance(list_node, basestring):
                        list_node = list_node.replace("\\", "\\\\")
                        list_node = '"%s"' % list_node
                    else:
                        if isinstance(list_node, dict):
                            # list_node = ''.join(_pretty(list_node, indent + ' ' * len(str(list_node) + ': {')))  # 计算下一层的indent
                            list_node = ''.join(
                                _pretty(list_node, indent + ' ' * len(':{')))
                        elif isinstance(list_node, list):
                            # list_node = ''.join(_pretty(list_node, indent + ' ' * len(str(list_node) + ': {')))  # 计算下一层的indent
                            list_node = ''.join(
                                _pretty(list_node, indent + ' ' * len(list_node)))  # 计算下一层的indent

                    # 因为python和json里面的boolean值大小写不一样,统一转换成小写的
                    if list_node is True:
                        list_node = 'true'
                    elif list_node is False:
                        list_node = 'false'

                    if i == 0:  # 开头,拼左花括号
                        if len(obj) == 1:  # 如果只有一个元素
                            yield '[%s]' % list_node
                        else:  # 如果超过了一个元素
                            yield '[%s,\n' % list_node
                    elif i == len(obj) - 1:  # 结尾,拼右花括号
                        yield '%s%s]' % (indent, list_node)
                    else:  # 中间
                        yield '%s%s,\n' % (indent, list_node)
        else:
            obj = str(obj)
            yield obj

    return ''.join(_pretty(obj, indent))


def equals(s1, s2):
    # i = ({'nickname': u'Default', 'sex': 1L},)
    # j = [{'nickname': u'Default', 'sex': 1L}]
    if (isinstance(s1, list) or isinstance(s1, tuple)) and (isinstance(s2, list) or isinstance(s2, tuple)):
        pass
    try:
        s1 = time_utils.time2long(s1)
        s2 = time_utils.time2long(s2)
        if isinstance(s1, unicode):
            s1 = s1.encode('utf8')
        if isinstance(s2, unicode):
            s2 = s2.encode('utf8')
        s1 = str2bool(s1)
        s2 = str2bool(s2)

        s1 = D_NULL.get(s1, s1)
        s2 = D_NULL.get(s2, s2)
        if str(s1) == str(s2):
            return True
        else:
            return False
    except:
        return False


def unequals(s1, s2):
    '''
    判断不等于
    :param s1:
    :param s2:
    :return:
    '''
    s1 = time_utils.time2long(s1)
    s2 = time_utils.time2long(s2)
    if isinstance(s1, unicode):
        s1 = s1.encode('utf8')
    if isinstance(s2, unicode):
        s2 = s2.encode('utf8')
    s1 = str2bool(s1)
    s2 = str2bool(s2)
    if str(s1) != str(s2):
        return True
    else:
        return False


def contains(s1, s2):
    if s1 == s2:
        return True
    else:
        return s1 in ContainsHelper(s2)

def uncontains(s1, s2):
    return s1 not in ContainsHelper(s2)

def compare(s1, s2, symbol):
    '''
    比较
    :param s1:
    :param s2:
    :param symbol:
    :return:
    '''
    # 如果
    s1 = time_utils.time2long(s1)
    s2 = time_utils.time2long(s2)
    try:
        express = "res = %s %s %s" % (s1, symbol, s2)
        # print express
        exec (express)
        return res
    except:
        return False


def str2bool(s_bool):
    '''
    #如果str跟bool有关系就转换为bool类型,没有就返回原始str
    :param s_bool:
    :return:
    '''
    d_bools = {'false': False, 'true': True}
    try:
        res = d_bools[s_bool.lower()]
    except:
        return s_bool
    else:
        return res


def is_str_inner(ss, re_exp):
    '''
    按正则匹配ss是否存在目标字符串
    :param re_exp:
    :param ss:
    :return:
    '''
    re1 = re.compile(re_exp)
    res = re1.findall(ss)
    if res != []:
        return True
    else:
        return False


def testqueue():
    q = Queue()  # 创建队列对象
    st = Stack()
    s = '(1+2)*(3-5)'

    for i in s:
        if i.isdigit():
            q.put(int(i))
        else:
            if st.is_empty():
                st.push(i)
            elif i == "(" or i == "（":
                st.push(i)
            elif i == ")" or i == "）":
                st.pop

    q.put(0)  # 在队列尾部插入元素
    q.put(1)
    q.put(2)
    print('LILO队列', q.queue)  # 查看队列中的所有元素
    print(q.get())  # 返回并删除队列头部元素
    print(q.queue)


def split_by_sep_list(s, l_sep):
    '''
    根据分隔符列表分割成list
    :param s:
    :param l_sep:
    :return:
    '''
    # re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', s)
    s_sep = fromat_sep_list_to_str(l_sep)
    return re.split('[%s]' % s_sep, s)


def fromat_sep_list_to_str(l_sep):
    '''
    格式化操作符并返回一个l_sep
    :return:
    '''
    a = {'\\': '\\\\', '-': '\\-'}
    for index, i in enumerate(l_sep):
        l_sep[index] = a.get(i, i)
    return ''.join(l_sep)


def findall_by_sep_list(s, l_s, l_protect_flag=None):
    '''
    获取所有符合seplist的sep放入一个list中
    :param s:
    :param l_s:
    :return:
    '''
    s_sep = fromat_sep_list_to_str(l_s)

    res = split_protect_list(s, l_protect_flag)
    l_res = []
    for i in res:
        if i[1] is False:
            a = re.compile('[%s]' % s_sep).findall(i[0])
            if a != []:
                l_res += a
    return l_res


def split_protect_list(s, l_protect_flag=None):
    '''
    把一个字符串按保护符合分割成n段 [(s1, is_protect),(s2, is_protect),(s3, is_protect)]
    :param s:
    :param l_protect_flag: ["保护符开头", "保护符结尾"]
    :return:
    '''
    res = []
    if l_protect_flag is None or l_protect_flag[0] not in s:
        res.append((s, False))
    else:
        start, end = 0, 0
        st = Stack()
        flag = False
        for index, c in enumerate(s):
            if c == l_protect_flag[0]:
                if index > 0 and flag is False:
                    res.append((s[start: index], False))
                if st.is_empty():
                    start = index
                st.push(c)
                flag = True
            elif c == l_protect_flag[1]:
                st.pop()
            if flag is True and st.is_empty():
                res.append((s[start: index + 1], True))
                start = index + 1
                flag = False
                if index == len(s) - 1:
                    break
            if index == len(s) - 1 and st.is_empty():
                res.append((s[start:], False))
    return res
    # while True:
    #     index = s.find(l_protect_flag[0])    #查找保护符
    #     if index == -1:
    #         break   #如果没有找到,跳出
    #     else:   #如果找到保护符下标
    #         temp = s[start:index]
    #         if index > 0:
    #             res.append((temp, False))
    #         st.push(l_protect_flag[0])

    return res


def merge_exp_to_list(l_value, l_oper):
    '''
    表达式合并
    :param l_value: 表达式中的值列表
    :param l_oper: 表达式操作符列表
    :return:
    '''

    q1 = Queue()
    q2 = Queue()

    for i in l_value:
        q1.put(i)
    for i in l_oper:
        q2.put(i)
    # print q1.queue
    # print q2.queue

    s = []
    while True:
        if q1.empty():
            if q2.empty():
                break
            else:
                s.append(q2.get())
        else:
            if q2.empty():
                s.append(q1.get())
            else:
                s.append(q1.get())
                s.append(q2.get())
    return s


def parse(source):
    cal = {"+": 1, "-": 1, "*": 2, "/": 2}
    cal1 = {"(": 0}
    result = []
    c = []
    e = ['+', '-', '*', '/', '%']
    slist = split_by_sep_list(source, e)
    ssep = findall_by_sep_list(source, e)
    slist = merge_exp_to_list(slist, ssep)
    for item in slist:
        if item.isdigit():
            result.append(item)
        elif not c and item in cal.keys():
            c.append(item)
            continue
        elif c and item in cal.keys():
            for x in range(c.__len__()):
                z = c[-1]
                temp = cal[z] if cal.has_key(z) else cal1[z]
                if temp >= cal[item]:
                    result.append(c.pop())
                else:
                    c.append(item)
                    break
            if not c:
                c.append(item)
        elif item == ")":
            for x in range(c.__len__()):
                if c[-1] == "(":
                    c.pop()
                    break
                else:
                    result.append(c.pop())
        elif item == "(":
            c.append(item)
        # print(result,c)
    for x in range(c.__len__()):
        result.append(c.pop())
    return result


def caculate(sourcestr):
    '''
    # 逆波兰式计算
    :param source:
    :return:
    '''
    try:
        int(sourcestr)
        return sourcestr
    except:
        source = parse(sourcestr)
        num = []
        try:
            for i in source:
                if i.isdigit():
                    num.append(i)
                else:
                    num1 = num.pop()
                    num2 = num.pop()
                    num.append(str(eval("%s%s%s" % (num2, i, num1))))
            return num[0]
        except:  # 如果计算失败就返回原值
            return sourcestr


def re_split(s_exp, l_sep, protect_flag=None):
    '''
    按多个字符分割字符串，如果有保护字符就不分割其中内容
    比如protect_flag='('就不分割()内的字符，
    比如protect_flag='"'就不分割""内的字符,
    如果protect_flat = ['${', '}']就不分割${}内的字符
    *如果protect_flat = ['${']就不分割${${ 内的字符(一般数组里面是两个元素的)
    :param s:   目标字符串
    :param l_sep:   按什么符号分割
    :param protect_flag:    保护字符
    :return:
    '''
    if protect_flag is None:
        s_fmt = fromat_sep_list_to_str(l_sep)
        res = re.split('[%s]' % s_fmt, s_exp)
    else:
        # D_BRACKETS = {'{': '}', '[': ']', '(': ')'}
        protect_flag_right = [D_BRACKETS.get(b) for b in protect_flag]
        res = []
        found_sep = []
        st = Stack()
        s = ""
        for i in s_exp:
            if i in l_sep:  # 如果是操作符
                # 判断栈是否为空
                if st.is_empty():  # 如果操作符不在保护区里面，就直接把他分割出来，并重置str
                    if s != '':
                        res.append(s.strip())
                        s = ''
                        found_sep.append(i)
                else:
                    s += i
            else:
                if i in protect_flag:  # 直接到第一个保护符，比保护符是'('就会略过[,{这些括号
                    st.push(i)
                elif i in protect_flag_right:
                    st.pop()
                s += i
        if s != '':
            res.append(s.strip())
    return res, found_sep

    # 原来的代码
    # if protect_flag is None:
    #     res = re.split('[%s]' % ''.join(l_sep), s)
    # else:   #如果有特殊保护分隔符
    #     l_flag = []
    #     if isinstance(protect_flag, str):
    #         l_flag = [protect_flag, D_BRACKETS.get(protect_flag, protect_flag)]
    #     elif isinstance(protect_flag, list):
    #         if len(protect_flag) == 1:
    #             l_flag = [protect_flag[0], D_BRACKETS.get(protect_flag[0], protect_flag[0])]
    #         elif len(protect_flag) == 2:
    #             l_flag = protect_flag
    #         else:
    #             raise Exception("protect_flag参数个数错误!")
    #     else:
    #         raise Exception("protect_flag参数类型错误!")
    #
    #     end = s.find(l_flag[0])   #先找第一个符合的
    #     s_sep = fromat_sep_list_to_str(l_sep)
    #     if end == -1:
    #         return re.split('[%s]' % s_sep, s)
    #     else:
    #         res = find(s, s_sep, l_flag, 0, end)
    # return res


def find(s, s_sep, l_flag, start=0, end=-1):
    res = []
    # 先根据分割第一部分
    p1 = re.split('[%s]' % s_sep, s[start: end])

    if p1 != []:
        if p1[-1] == '':  # 判断是否有分隔符sep衔接flag的比如“1+(xxx)”
            p1 = p1[0:-1]
        res += p1  # 添加p1
    res[-1] += s[end:]
    return res


def find_flag_list(s, flag, index=None, res=[]):
    '''
    获取
    :param sub:
    :param flag:
    :return:
    '''
    i = s.find(flag, index)
    if i == -1:
        return res
    else:
        res.append(i)
        return find_flag_list(s, flag, i + len(flag), res)


def get_sql_params(exp, flag):
    '''
    获取 flag内的数据
    :param exp:
    :return:
    '''
    st = Stack()
    l_index = []
    temp = False
    for index, i in enumerate(exp):
        if i == flag:
            st.push(i)
            if temp is False:
                l_index.append(index + 1)
            temp = True
        elif i == D_BRACKETS.get(flag):
            st.pop()
        if temp is True and st.is_empty():
            l_index.append(index)
            break
    if l_index != []:
        res = exp[l_index[0]:l_index[1]]
    else:
        res = exp
    res = res[1:-1]
    res = res.replace('\\', '')
    return [res]


def list_item_trans_str(l):
    '''
    单结构list元素转str
    :param l:
    :return:
    '''
    for index, i in enumerate(l):
        if isinstance(i, str):
            pass
        else:
            try:
                l[index] = str(i)
            except:
                print ("list元素转str失败")
                pass


def findexp(str_variable):
    # 字符变量${var}
    # str_variable = "ddddddddddddddd =${var1}.aaaaa.xx.xx"
    re_variable = re.compile(r'^[a-zA-Z\_][0-9a-zA-Z\_]*')
    a = re.findall(re_variable, str_variable)
    if a != []:
        return a

    # 变量.jsonpath
    # 字符变量${var}
    # str_variable = "ddddddddddddddd${var1}.aaaaa.xx.xx"
    re_variable = re.compile(r'\$\{[a-zA-Z\_][0-9a-zA-Z\_]*\}\.\S*')
    a = re.findall(re_variable, str_variable)
    if a != []:
        return a

    # redis
    # str_variable = "ddddddddddddddd$.redis.xxxx.query()"
    re_redis = re.compile(r'\$\.redis\.[_a-zA-Z][_0-9a-zA-Z]*\(\)')
    a = re.findall(re_redis, str_variable)
    if a == []:
        re_redis2 = re.compile(r'\$\.redis\.[_a-zA-Z][_0-9a-zA-Z]*\.[_a-zA-Z][_0-9a-zA-Z]*\(\)')
        a = re.findall(re_redis2, str_variable)
    if a != []:
        return a

    # mysql
    # str_variable = "ddddddddddddddd$.mysql.xxxx.query()"
    re_redis = re.compile(r'\$\.mysql\.[_a-zA-Z][_0-9a-zA-Z]*\(\)')
    a = re.findall(re_redis, str_variable)
    if a == []:
        re_redis2 = re.compile(r'\$\.mysql\.[_a-zA-Z][_0-9a-zA-Z]*\.[_a-zA-Z][_0-9a-zA-Z]*\(\)')
        a = re.findall(re_redis2, str_variable)
    if a != []:
        return a

    # method方法
    # str_variable = "ddddddddddddddd$.Fun(${aa}, 1, 2)"
    re_variable = re.compile(r'\$\.[_a-zA-Z][_a-zA-Z0-9]*\(.*\)')
    a = re.findall(re_variable, str_variable)
    if a != []:
        return a

    # 字符变量${var}
    # str_variable = "ddddddddddddddd${var1}.aaaaaa"
    re_variable = re.compile(r'(\$\{[a-zA-Z\_][0-9a-zA-Z\_]*\})')
    a = re.findall(re_variable, str_variable)
    if a != []:
        return a
    raise ExpressException()


def testsplit(exp, l_sep, protect_flag=None):
    if protect_flag is None:
        s_fmt = fromat_sep_list_to_str(l_sep)
        res = re.split('[%s]' % s_fmt, exp)
    else:
        # D_BRACKETS = {'{': '}', '[': ']', '(': ')'}
        protect_flag_right = [D_BRACKETS.get(b) for b in protect_flag]
        res = []
        st = Stack()
        s = ""
        for i in exp:
            if i in l_sep:  # 如果是操作符
                # 判断栈是否为空
                if st.is_empty():  # 如果操作符不在保护区里面，就直接把他分割出来，并重置str
                    if s != '':
                        res.append(s.strip())
                        s = ''
                else:
                    s += i
            else:
                if i in protect_flag:  # 直接到第一个保护符，比保护符是'('就会略过[,{这些括号
                    st.push(i)
                elif i in protect_flag_right:
                    st.pop()
                s += i
        if s != '':
            res.append(s.strip())
    return res


def mycmp(n, m):
    """用来比较list中嵌dict，或tuple嵌dict
    这里的dict为单层结构
    """
    try:
        for i, item in n:
            for k, v in item.items():
                if str(v) == str(m[i][k]):
                    continue
                else:
                    return False
    except:
        return False

def remove_host_http_prefix(host):
    '''
    规范化host，去掉前缀进行匹配使用，如果同时使用http和https会造成误差
    :param host:
    :return:
    '''
    if host.startswith('http://'):
        host = host[7:]
    if host.startswith('https://'):
        host = host[8:]
    return host

if __name__ == "__main__":
    L_SEP = ['>=', '<=', '!=', '==', '=', '>', '<']
    s = '$.data[0].book.books[?(@.book_id=="48dccc16577df829cf1623e14660cd6f")]'
    a = my_split2(L_SEP, s, tag='[')
    for i in a:
        print (i)
