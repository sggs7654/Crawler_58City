# -*- coding: utf-8 -*-

import scrapy
import requests


class MainSpider(scrapy.Spider):
    name = '58'

    def start_requests(self):
        """
        访问城市切换页面
        :yield: 城市切换页面
        """
        yield scrapy.Request(url='https://www.58.com/changecity.html', callback=self.parse_city_href)

    def parse_city_href(self, response):
        """
        在城市切换页面中，解析并合成各城市租房页面的地址
        :yield: 各城市的租房页面
        """
        city_list = response.xpath("//script[position()=3]/text()").re(r':"(.*?)\|.*?"')
        url_template = 'https://{}.58.com/chuzu/'
        url_list = [url_template.format(city) for city in city_list]
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for url in url_list[0:1]:  # 先爬一个作为测试
            yield scrapy.Request(url=url, callback=self.parse_house_list)

    def parse_house_list(self, response):
        """
        在租房页面，解析广告标题，房间信息，租房价格三项数据
        """
        li_list = response.xpath('//li[@class="house-cell"]')
        titles, rooms, prices = [], [], []
        for li in li_list:
            titles.append(li.xpath('.//a[@class="strongbox"]/text()').re(r'\s*(.*?)\s{3,}'))
            rooms.append(li.xpath('.//p[@class="room"]/text()').get())
            prices.append(li.xpath('.//b[@class="strongbox"]/text()').get())


