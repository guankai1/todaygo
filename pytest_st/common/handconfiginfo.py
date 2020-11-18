from os import path
from common.configparserhandler import *

# 配置读取器
configParseHandler = ''
# 运行根目录
base_dir = path.dirname(path.dirname(__file__))
# 测试环境配置文件保存目录
test_env_dir = path.join(base_dir, 'configs', 'env_dev2.ini')
# 测试结果保存文件
test_result_file = path.join(base_dir, 'log', 'data.json')

print(test_env_dir)
configParseHandler = ConfigparserHandler(test_env_dir)

todayGo_host = configParseHandler.get_data('host_go', 'host')
print(todayGo_host)
