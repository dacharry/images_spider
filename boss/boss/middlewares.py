# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from boss.models import ProxyModel
import json
import requests

class UseragentDownlaoderMiddleware(object):
    User_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (X11; U; Linux x86_64; en; rv:1.9.0.8) Gecko/20080528 Fedora/2.24.3-4.fc10 Epiphany/2.22 Firefox/3.0',
        'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.User_agents)
        request.headers['User-Agent'] = user_agent


class IpProxyDownloaderMiddleware(object):
    def __init__(self):
        self.status = False


    def process_request(self, request, spider):
        if self.status:
            proxy = self.get_proxyIp()
            print("*"*50)
            print(proxy.proxy)
            request['proxy'] = proxy.proxy
            self.status = False

    def get_proxyIp(self):
        proxy_api = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=4d9d6f7844ac4ff0ba9741196055ffb0&orderno=YZ20193105820IhjYI2&returnType=2&count=1"
        response = requests.get(proxy_api)
        data = json.loads(response.text)
        data = data['RESULT'][0]
        print(data)
        proxy = ProxyModel(data)
        return proxy

    def process_response(self, request,response, spider):

        if response.status == '403':
            self.status = True
        return response