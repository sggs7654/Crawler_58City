# -*- coding: utf-8 -*-
import redis
import logging


class Crawler58CityPipeline(object):

    def __init__(self):
        self.db = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def process_item(self, item, spider):
        data = "【{}】{}".format(item['price'], item['title'])
        self.db.sadd(item.table, data)
