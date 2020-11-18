import copy
import pytest
import requests
import os
from common.logging_get import LogHandler
logging = LogHandler().log()
from common.handconfiginfo import *
from todayGogogo.testdata.today_go import _today_go
from todayGogogo.conftest import auth_token

login_data = {"account":"gaixm@tiens.com","password":"Xm130130","terminalType":"3"}
uri = configParseHandler.get_data('host_go', 'host')
url_path = _today_go()

querry_country_param = {}
def querry_county():
    testData = copy.deepcopy(querry_country_param)
    return testData

def auth_tokens():
    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8"
               }

    post_response = requests.post(url=uri + url_path.Login_url,
                                  json=login_data,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    logging.info(resp_payload)
    assert resp_payload['code'] == '0'  # to be defined.
    auth_tokens = resp_payload['data']['token']
    print(auth_tokens)
    return auth_tokens

def test_get_data():
    global auth_token
    print(auth_token)
    return auth_token
"""
class tokens_exp():
  def __init(self, auth_token):
        self.auth_token = auth_token

  def get_list(self):
    #token_param=test_get_data(auth_token)
    print(self.auth_token)
    return self.auth_token
"""




if __name__ == '__main__':
 pytest.main(['-s', '-q', 'querry_count_data.py'])




