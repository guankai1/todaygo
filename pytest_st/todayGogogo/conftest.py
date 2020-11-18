import pytest
import requests
import os
from common.logging_get import LogHandler
logging = LogHandler().log()
from common.handconfiginfo import *
from todayGogogo.testdata.today_go import _today_go

login_data = {"account":"gaixm@tiens.com","password":"Xm130130","terminalType":"3"}
uri = configParseHandler.get_data('host_go', 'host')
#login_url = "/user/web/pc/login/accountPwdLogin"
url_path = _today_go()


@pytest.fixture(scope="session", autouse=True)
def auth_token():
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
    auth_token = resp_payload['data']['token']
    yield auth_token

    #print(auth_token)
    #return auth_token

#auth_token()

