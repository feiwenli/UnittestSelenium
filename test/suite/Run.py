# -*- coding:utf-8 -*-
import unittest

import os

from utils.HTMLTestRunner import HTMLTestRunner
import time
from utils.config import REPORT_PATH, CASE_PATH
from utils.mail import Mail
from utils.log import Logger

from BeautifulReport import BeautifulReport

# BeautifulReport Git https://github.com/TesterlifeRaymond/BeautifulReport
logger = Logger(__name__).get()


class MSuit:
    def __init__(self):
        self.suites = unittest.defaultTestLoader.discover(CASE_PATH, pattern='Test*.py')
        self.report_name = time.strftime("%Y%m%d%H%M", time.localtime()) + 'result.html'

    def run(self):
        fp = open(os.path.join(REPORT_PATH , self.report_name), 'wb')
        runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'测试用例执行情况')
        runner.run(self.suites)
        logger.info('run suits success')
        fp.close()
        logger.info(self.report_name+' is closed.')

        result = BeautifulReport(self.suites)
        result.report(filename=self.report_name, description='测试deafult报告', log_path='report')

        # 发邮件
        Mail(self.report_name).send()

MSuit().run()
