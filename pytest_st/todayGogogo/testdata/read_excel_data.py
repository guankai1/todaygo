from common.handleExcel.file_utils import *
import sys


cur_path='C:\\Users\\qqq\\PycharmProjects\\pytest_st\\todayGogogo\\testdata\\'
"""
list_case = case_xlsx_loader(
    'C:\\Users\\qqq\\PycharmProjects\\pytest_st\\todayGogogo\\testdata\\todaygo_testcase_offline.xlsx', sheets='服务相关',
    name=None, tags=None)
print(type(list_case))
print(list_case[0][0])
print(cur_path)
"""
def get_case(filename,sheetname=None,tag=None):
    path = cur_path + filename
    #tag = set(tag)
    list_case=case_xlsx_loader(path,sheets=sheetname,tags=tag)
    print(type(tag))
    print(tag)
    print(list_case)
    print(type(list_case[0]))
    print(len(list_case))
    return list_case

str = 'todaygo_testcase_offline.xlsx'
get_case(str,sheetname='服务相关',tag={'p1'})




