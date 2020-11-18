
from common.requestHandler import RequestHandler
from common.handconfiginfo import *
from todayGogogo.testdata.today_go import _today_go
#日志收集器
from common.logging_get import LogHandler
logging = LogHandler().log()

class TodayGoShop(object):
    """
        统一上报ID自动化

    """

    def __init__(self):
        self.host = configParseHandler.get_data('host_go', 'host')
        self.path = _today_go()

    def get_country_go(self,param):
        """辐射国接口
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.path.Querry_Country_INFO
        code, ret = RequestHandler(url,param).post_json()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.path.Querry_Country_INFO
