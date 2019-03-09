# -*- coding=utf-8 -*-

import requests
import json

import time

from utils.config import TestData, API_DATA_FILE, ENV


# 自定义身份验证
class BearerAuth:
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = 'bearer' + self.token
        return request


class SendRequest:
    def __init__(self):

        self.env = ENV
        self.max_time = 30
        # HTTP 头部大小写不敏感
        self.headers_simple = {'Content-Type': 'application/json;charset=UTF-8',
                               'Accept': 'application/json, text/plain, */*'}
        self.data = TestData(file=API_DATA_FILE, env=self.env)

        self.login_json = self.login_normal()
        self.access_token = self.login_json.get('resp')[0].get('access_token')
        self.user_env = self.login_json.get('resp')[0].get('env')

        # self.headers_auth = {'Content-Type': 'application/json;charset=UTF-8',
        #                        'Accept': 'application/json, text/plain, */*',
        #                      'Authorization': 'bearer'+self.access_token}

    def __to_list(self, str):
        if str == "":
            return []
        else:
            return str.split(',')

    def search_description_condition_base(self, page=1, page_size=24, description="", insite_description="",
                                          color="", size="", season="", material="", identity="", sex="",
                                          rank="overall", low=0, high=0):

        color = self.__to_list(color)
        season = self.__to_list(season)
        size = self.__to_list(size)
        material = self.__to_list(material)
        identity = self.__to_list(identity)
        sex = self.__to_list(sex)

        payload = {"pageInfo": {"page": page, "pageSize": page_size}, "description": description,
                   "insiteDescription": insite_description, "color": color, "size": size,
                   "season": season, "material": material, "identity": identity,
                   "sex": sex, "rank": rank, "priceRange": {"low": low, "high": high}}

        url = self.data.get('url_d') + '/hmall-sc-service/search/searchWithDescriptionAndConditions'

        request = requests.post(url, data=json.dumps(payload), headers=self.headers_simple, timeout=self.max_time)

        if request.status_code != 200:
            request = requests.post(url, data=json.dumps(payload), headers=self.headers_simple, timeout=self.max_time)
            request.raise_for_status()

        return request.json()

    def login_normal(self):
        print(self.max_time)
        payload = {"customerId": self.data.get('phone'),
                   "pwd": self.data.get('password'),
                   "t": time.time() * 100}

        url = self.data.get('url_d') + '/hmall-ur-service/login/normal'

        request = requests.post(url, data=json.dumps(payload), headers=self.headers_simple, timeout=self.max_time)

        if request.status_code != 200:
            request = requests.post(url, data=json.dumps(payload), headers=self.headers_simple, timeout=self.max_time)
            request.raise_for_status()

        if not request.json().get('success'):
            print(request.json())
            raise Exception('>> login failure <<')
        else:
            print('>> login success <<')
        # print(request.text)
        # print(request.json())
        # print(request.status_code)
        # print(request.raise_for_status())
        return request.json()

    def user(self):

        url = self.data.get('url_d') + '/auth/user'

        request = requests.get(url, headers=self.headers_simple, auth=BearerAuth(self.access_token),
                               timeout=self.max_time)

        if request.status_code != 200:
            request = requests.get(url, headers=self.headers_simple, auth=BearerAuth(self.access_token),
                                   timeout=self.max_time)
            request.raise_for_status()

        print(request.text)

        return request.json()

# SendRequest().user()
