#!/usr/bin/env bash

rm -rf allure-report/*

#pytest -s todayGogogo/testcase/test_feature.py  -m P0 --alluredir allure-report
pytest -s todayGogogo/testcase/test_feature.py --alluredir allure-report
allure generate allure-report -o C:/Users/qqq/PycharmProjects/pytest_st/report/ --clean
