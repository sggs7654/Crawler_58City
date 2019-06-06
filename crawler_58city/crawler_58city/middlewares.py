# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests,logging
URL = 'http://127.0.0.1:5000/random'


class RandomUAMiddleware(object):
    def __init__(self):
        self.user_agent = UserAgent().random

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = requests.get(URL).text
        request.meta["proxy"] = proxy

