# -*- coding: utf-8 -*-

from fake_useragent import UserAgent


class RandomUAMiddleware(object):
    def __init__(self):
        self.user_agent = UserAgent().random

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent

