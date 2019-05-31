# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseInfo(scrapy.Item):
    table = '58city'
    title = scrapy.Field()
    price = scrapy.Field()

