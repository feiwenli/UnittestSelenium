# -*- coding:utf-8 -*-

from os import path
from utils.read_file import ReadYml, ReadCsv
import os
import platform

ENV = 'HKPROD'
PLATFORM = 'PC'

'''路径配置'''

BASE_PATH = path.dirname(path.dirname(path.abspath(__file__)))
CONFIG_PATH = path.join(BASE_PATH, 'config')
CONFIG_FILE = path.join(CONFIG_PATH, 'Config.yml')
REPORT_PATH = path.join(BASE_PATH, 'report')

cur_sys = platform.system()
if cur_sys == 'Windows':
    DRIVER_PATH = path.join(BASE_PATH, 'driver')
    CHROME_DRIVER_FILE = path.join(DRIVER_PATH, 'chromedriver.exe')
elif cur_sys == 'Linux':
    DRIVER_PATH = path.join('/usr', 'bin')
    CHROME_DRIVER_FILE = path.join(DRIVER_PATH, 'chromedriver')
else:
    print('unknown system %s.' %cur_sys)

LOG_PATH = path.join(BASE_PATH, 'log')
DATA_PATH = os.path.join(BASE_PATH, 'data')
UI_DATA_FILE = os.path.join(DATA_PATH, 'DataForUI.csv')
API_DATA_FILE = os.path.join(DATA_PATH, 'DataForAPI.csv')
TEST_PATH = os.path.join(BASE_PATH, 'test')
CASE_PATH = os.path.join(TEST_PATH, 'case')

class Config:
    def __init__(self, config=CONFIG_FILE, key='mail'):
        # print(CONFIG_FILE)
        self.__config = ReadYml(config).data
        # self.__config = ReadYml(config).data
        self.key = key

    def get(self, var):
        # yml 文件以dict的形式存储，按环境分类
        return self.__config.get(self.key).get(var)


# Config(env='HKPROD').get('url_login')


class TestData:
    def __init__(self, file=UI_DATA_FILE, env='HKPROD'):
        self.__data = ReadCsv(file, env).data

    def get(self, var):
        return self.__data.get(var)
