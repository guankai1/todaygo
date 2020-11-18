# -*- coding: utf-8 -*-

import allure
import os
import pytest
from common.logging_get import  LogHandler
import time
import requests
from todayGogogo.testdata.get_interface import TodayGoShop
from todayGogogo.testdata.querry_count_data import querry_county
from todayGogogo.testdata.read_excel_data import get_case
logging = LogHandler().log()


def get_desc_as_test_id(fixture_value):
        """约定测试数据集第一个值为用例描述，把这个参数抽取出来作为test id的最后一部分
        """
        return fixture_value[0]


class TestTodayGo(object):


    @pytest.fixture()
    def get_cases_params(params=[i for i in get_case()]):
        """test_querry_country用例的测试数据集合输入
        """
        return querry_county()
    @pytest.mark.P0
    @pytest.mark.gexiaoming
    def test_cases_excel(self ,get_querry_county_params):
        testdata = get_querry_county_params
        logging.info(testdata)
        ret ,url = TodayGoShop().get_country_go(testdata)

        assert ret['code'] == '0'
