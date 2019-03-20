# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
import requests
import json
import time
from fake_useragent import UserAgent


# class MaitianDownloaderMiddleware(object):
#
#     def process_request(self, request, spider):
#         ua = UserAgent()
#         request.headers['User-Agent'] = ua.random
#         proxy = self.get_proxy()
#         request.meta['proxy'] = proxy
#         return None
#
#     def process_response(self, request, response, spider):
#         if response.status != 200:
#             proxy = self.get_proxy()
#             request.meta['proxy'] = proxy
#             return request
#         return response
#
#     def get_proxy(self):
#         while True:
#             time.sleep(1)
#             response = requests.get(
#                 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=4d9d6f7844ac4ff0ba9741196055ffb0&orderno=YZ20193105820IhjYI2&returnType=2&count=1')
#             data = json.loads(response.text)['RESULT'][0]
#             print(data)
#             if type(data) != dict:
#                 continue
#             proxy = 'http://' + data['ip'] + ':' + data['port']
#             break
#         print(proxy, "*" * 39)
#         return proxy


class RandomUAMiddleware(object):
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random


class ProxyMiddleware(object):
    proxy_list = [
        'http://183.15.122.53:23388',
        'http://180.123.180.167:34356',
        'http://42.59.103.101:29107',
        'http://125.123.122.82:34765',
    ]

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxy_list)
        print(request.meta['proxy'])
