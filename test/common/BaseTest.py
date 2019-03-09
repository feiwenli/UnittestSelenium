# -*- coding=utf-8 -*-
import time
import unittest

from selenium import webdriver

from api.send_request import SendRequest
from utils.config import Config, DRIVER_PATH, TestData, ENV, PLATFORM, CHROME_DRIVER_FILE
from os import path

from utils.log import Logger

logger = Logger(__name__).get()

class BaseTest(unittest.TestCase):

    def setUp(self):

        self.config = Config()
        self.test_data = TestData(env=ENV)

        self.options = webdriver.ChromeOptions()

        if PLATFORM == 'H5':
            # 模拟移动设备
            self.mobile_emulation = {'deviceName':'iPhone 6'}
            self.options.add_experimental_option("mobileEmulation", self.mobile_emulation)

        # for error:exited abnormally
        self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(CHROME_DRIVER_FILE, chrome_options=self.options)

        self.driver.maximize_window()
        self.driver.get(self.test_data.get('url'))
        time.sleep(3)

    # for pc
    def setCookies(self):
        self.driver.add_cookie({'name': 'access_token', 'value': SendRequest().access_token})
        time.sleep(3)
        self.driver.refresh()
        time.sleep(3)

    # for h5
    def setStorage(self):
        request = SendRequest()
        js_1 = "window.localStorage.setItem('Uniqlo_token','" + request.access_token + "');"
        js_2 = "window.localStorage.setItem('Uniqlo_userEnv','" + request.user_env + "');"
        self.driver.execute_script(js_1)
        self.driver.execute_script(js_2)
        time.sleep(3)
        self.driver.refresh()
        time.sleep(3)

    def tearDown(self):
        self.driver.quit()
        logger.info('close browser')


# BaseTest()