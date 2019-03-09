# -*- coding=utf-8 -*-

import logging

from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

import os

import time

from utils.config import Config, LOG_PATH


class Logger:
    def __init__(self, name):
        self.config = Config(key='log')
        self.logger = logging.getLogger(name)

    def get(self):
        if not self.logger.handlers:
            self.logger.setLevel(level=self.config.get('level'))
            # handler = logging.FileHandler(os.path.join(LOG_PATH, self.config.get('file_name')))

            # 设置：最多备份3个日志文件，每个日志文件最大1K
            # handler = RotatingFileHandler(os.path.join(LOG_PATH, self.config.get('file_name')), maxBytes=1 * 1024,
            #                               backupCount=self.config.get('backup'))

            # 每天重新创建一个日志文件，最多保留backup_count份
            # “S”: Seconds
            # “M”: Minutes
            # “H”: Hours
            # “D”: Days
            # “W”: Week day (0=Monday)
            # “midnight”: Roll over at midnight
            # interval 是指等待多少个单位when的时间后，Logger会自动重建文件
            handler = TimedRotatingFileHandler(
                os.path.join(LOG_PATH, time.strftime("%Y%m%d", time.localtime()) + self.config.get('file_name')),
                when='D', interval=1, backupCount=self.config.get('backup'), delay=True, encoding='utf-8')
            handler.setLevel(level=self.config.get('file_level'))
            formatter = logging.Formatter(self.config.get('pattern'))
            handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setLevel(level=self.config.get('console_level'))
            console.setFormatter(formatter)

            self.logger.addHandler(handler)
            self.logger.addHandler(console)

        return self.logger


# logger = Logger(__name__).get()
# logger.debug('debug')
# logger.info('info')
# logger.warning('warning')
# logger.error('error')
