# -*- coding:utf-8 -*-

import time
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data import myXpath
from test.common.BaseTest import BaseTest
from utils.config import ENV, PLATFORM
from utils.log import Logger

logger = Logger(__name__).get()

class Login(BaseTest):
    def setUp(self):
        super(Login, self).setUp()

    @unittest.skipIf(ENV == 'CNPROD' or PLATFORM == 'H5', 'run test for %s and %s' %(ENV, PLATFORM))
    def test_loginByPassword(self):

        self.url_login = self.test_data.get('url_login')
        driver = self.driver
        driver.get(self.url_login)

        element = WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located(
            (By.XPATH, myXpath.INPUT_USER_NAME)))
        element.click()
        element.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE)
        element.send_keys(self.test_data.get('phone'))
        time.sleep(1)

        driver.find_element(By.XPATH, myXpath.INPUT_PWD).send_keys(self.test_data.get('password'))
        time.sleep(1)

        driver.find_element(By.XPATH, myXpath.BUTTON_SUBMIT).click()
        time.sleep(1)

        WebDriverWait(driver, 10, 1).until(EC.invisibility_of_element_located((
            By.XPATH, myXpath.TOP_BY_TEXT.format(self.test_data.get('log_out')))))

        logger.info('login success')

    @unittest.skipIf(PLATFORM == 'PC', 'run test for %s and %s' %(ENV, PLATFORM))
    def test_setStorage(self):

        super().setStorage()
        WebDriverWait(self.driver, 10, 1).until(EC.invisibility_of_element_located((
            By.XPATH, myXpath.WISH_LIST_BTN))).click()
        WebDriverWait(self.driver, 10, 1).until(EC.presence_of_element_located((
            By.XPATH, myXpath.WISH_LIST_HEAD)))

        logger.info('login success')

    @unittest.skipIf(ENV == 'HKPROD' or PLATFORM == 'H5', 'run test for %s and %s' %(ENV, PLATFORM))
    def test_setCookies(self):

        super().setCookies()
        WebDriverWait(self.driver, 10, 1).until(EC.invisibility_of_element_located((
            By.XPATH, myXpath.TOP_BY_TEXT.format(self.test_data.get('log_out')))))

        logger.info('login success')


    def tearDown(self):
        super().tearDown()


# if __name__ == '__main__':
#     # unittest.main() # 按case的名称执行

#     # 构造测试集
#     suite = unittest.TestSuite()
#     suite.addTest(Login("test_loginByPassword"))
#     suite.addTest(Login("test_setStorage"))
#     suite.addTest(Login("test_setCookies"))


#     # 执行
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
