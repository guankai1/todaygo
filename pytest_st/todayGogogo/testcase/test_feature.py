# -*- coding: utf-8 -*-

import allure
import os
import pytest
from common.logging_get import  LogHandler
import time
import requests
from todayGogogo.testdata.get_interface import TodayGoShop
from todayGogogo.testdata.querry_count_data import querry_county

logging = LogHandler().log()


def get_desc_as_test_id(fixture_value):
        """约定测试数据集第一个值为用例描述，把这个参数抽取出来作为test id的最后一部分
        """
        return fixture_value[0]


class TestTodayGogogo(object):


    #@pytest.fixture(params=[("one","1111"),("two","2222"),("three","3333")],ids=get_desc_as_test_id)
    @allure.feature('test_module_01')
    def test_case_01(self,request):
        """
        用例描述：Test case 01
        """
        data =request[1]
        logging.info("testtest")
        assert 0 == 0
        assert data =="1111"


    @allure.feature('test_module_02')
    @pytest.mark.P5
    def test_case_02(self):
        """
        用例描述：Test case 02
        """

        assert 0 == 0
    @pytest.mark.P5
    @pytest.mark.gexiaoming
    def test_base_baidu(self):
        result = requests.get(url="https://wwww.baidu.com")
        logging.info(result)
        code = result.status_code
        assert 200 == code

    @pytest.fixture()
    def get_querry_county_params(self):
        """test_querry_country用例的测试数据集合输入
        """
        return querry_county()
    @pytest.mark.P0
    @pytest.mark.gexiaoming
    def test_querry_country(self,get_querry_county_params):
        testdata = get_querry_county_params
        logging.info(testdata)
        ret,url = TodayGoShop().get_country_go(testdata)

        assert ret['code'] == '0'

    @pytest.fixture()
    def get_customer_login_params(self):
        """test_C端登录的，用例的测试数据集合输入
        """
        return querry_county()
    @pytest.mark.P0
    @pytest.mark.gexiaoming
    def test_login_customer(self,get_customer_login_params):
        testdata = get_customer_login_params
        logging.info(testdata)
        ret,url = TodayGoShop().get_country_go(testdata)

        assert ret['code'] == '0'


if __name__ == '__main__':
    os.system('rm -rf allure-report/*')
    pytest.main(['-s', '-q', '--alluredir', 'pytest_st/allure-report/'])
    time.sleep(2)
    os.system('allure generate allure-report -o C:/Users/qqq/PycharmProjects/pytest_st/report/ --clean')
    logging.info("完成")
    #pytest C:\Users\qqq\PycharmProjects\pytest_st\test_python.py  --alluredir=./allure-results/
    #pytest - s common/test_feature.py --alluredir pytest_st/report/html
    #allure generate pytest_st / report / html - o C: / Users / qqq / PycharmProjects / pytest_st / report / --clean




