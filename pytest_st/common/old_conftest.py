import pytest
import requests
import os

authentication_url_path = "/v1/tokens"
login_url = "/user/web/pc/login/accountPwdLogin"

json_login = {
   "authType": "password",
   "params": {
       "username": "gexiaoming",
        "password": "jixlb2tIrjF5t/bYQTXz4Q=="
    }
}

login_data = {"account":"gaixm@tiens.com","password":"Xm130130","terminalType":"3"}


def pytest_addoption(parser):
    parser.addoption("--ip", action="store", default="XX.XX.XX.XX", help="please input target VM ip.")
    parser.addoption("--port", action="store", default="api", help="please input target service port.")


@pytest.fixture(scope="session", autouse=True)
@pytest.mark.P0
def ip(request):
    print(request.config.getoption("--ip"))
    return request.config.getoption("--ip")


@pytest.fixture(scope="session")
def port(request):
    return request.config.getoption("--port")


@pytest.fixture(scope="session")
def uri(ip,port):
    uri = "http://%s/%s" % (ip, port)
    return uri

"""
@pytest.fixture(scope="session")
def auth_token(uri):
    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8"
               }

    post_response = requests.post(url=uri + authentication_url_path,
                                  json=json_login,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    auth_token = resp_payload['data']['key']

    return auth_token
"""
@pytest.fixture(scope="session")
def auth_tokens(uri):
    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8"
               }

    post_response = requests.post(url=uri + authentication_url_path,
                                  json=json_login,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    auth_tokens = resp_payload['data']['key']

    return auth_tokens


@pytest.fixture(scope="session")
def headers(uri):
    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8"
               }

    post_response = requests.post(url=uri + authentication_url_path,
                                  json=json_login,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    auth_token = resp_payload['data']['key']

    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8",
               "T-AUTH-TOKEN": auth_token}
    return headers

if __name__ == '__main__':
    #pytest.main(["old_conftest.py::test_ip"])
    os.system('pytest -s old_conftest.py')

