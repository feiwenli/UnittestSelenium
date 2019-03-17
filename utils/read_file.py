# -*- coding=utf-8 -*-
import csv

import yaml
from os import path


# BASE_PATH = path.dirname(path.dirname(path.abspath(__file__)))
# CONFIG_PATH = path.join(BASE_PATH, 'config')
#
# yamlPath = path.join(CONFIG_PATH, 'config.yml')
#
# f = open(yamlPath, 'r', encoding='utf-8')
# d = yaml.load(f.read())
#
# print(d)
# print(d.get('HKPROD').get('phone'))


class ReadYml:
    def __init__(self, yml_path):
        if path.exists(yml_path):
            self.yml_path = yml_path
            # self.file = open(ymlPath, 'r', encoding='utf-8')
        else:
            raise FileNotFoundError('yml 文件路径不存在！')
        self._data = None

    @property
    def data(self):

        with open(self.yml_path, 'r', encoding='utf-8') as f:
            # self._data = list(yaml.safe_load_all(f))
            self._data = yaml.load(f)
        return self._data


class ReadCsv:
    def __init__(self, csv_path, env):
        if path.exists(csv_path):
            self.csv_path = csv_path
        else:
            raise FileNotFoundError('csv 文件路径不存在！')
        # self.file = open(csvPath, 'r')
        self.env = env
        self.__dic = {}

    @property
    def data(self):
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)  # 可迭代对象
            # 读取第一行，判断环境
            head_row = next(reader)
            list_num = 0
            for x in head_row:
                if x == self.env:
                    break
                list_num += 1
            # 存取数据
            for row in reader:
                self.__dic[row[1]] = row[list_num]
        return self.__dic


# if __name__ == '__main__':
#
#     d = ReadCsv('D:/code/python/UnittestFrame/data/DataForUIDataForUI.csv', 'CNPROD').data
#     print(type(d))
#     for k, v in d.items():
#         print(k, v)
