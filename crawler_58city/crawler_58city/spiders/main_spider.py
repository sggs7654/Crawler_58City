# -*- coding: utf-8 -*-

import scrapy
import base64
from fontTools.ttLib import TTFont
import io
import re
from scrapy.selector import Selector
from crawler_58city.items import HouseInfo


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
        for url in url_list[0:1]:  # 先爬一个城市作为测试
            yield scrapy.Request(url=url, callback=self.parse_house_list)

    def parse_house_list(self, response):
        """
        在租房页面，解析广告标题和租房价格
        """
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        new_response = self.cracking_font_encryption(response)
        li_list = new_response.xpath('//li[@class="house-cell"]')
        # titles, prices = [], []
        for li in li_list:
            # titles.append(li.xpath('.//a[@class="strongbox"]/text()').re(r'\s*(.*?)\s{3,}'))
            # prices.append(li.xpath('.//b[@class="strongbox"]/text()').get() + "元/月")
            title = li.xpath('.//a[@class="strongbox"]/text()').re(r'\s*(.*?)\s{3,}')[0]
            price = li.xpath('.//b[@class="strongbox"]/text()').get() + "元/月"
            item = HouseInfo(title=title, price=price)
            yield item
        """
        翻页，直到没有“下一页”的链接
        """

    def cracking_font_encryption(self, response):
        """
        应对字体反爬
        :param response: scrapy返回的response
        :return: 破解字体反爬后的response
        """
        # 抓取加密字符串
        base64_str = response.xpath('//head/script[position()=2]/text()').re(r"base64,(.*?)'\) format")[0]
        b = base64.b64decode(base64_str)
        font = TTFont(io.BytesIO(b))
        bestcmap = font['cmap'].getBestCmap()
        newmap = dict()  # 计算正常字体的映射字典
        for key in bestcmap.keys():
            value = int(re.search(r'(\d+)', bestcmap[key]).group(1)) - 1
            key = hex(key)
            newmap[key] = value
        response_ = response.text  # 根据映射字典替换反爬字符
        for key, value in newmap.items():
            key_ = key.replace('0x', '&#x') + ';'
            if key_ in response_:
                response_ = response_.replace(key_, str(value))
        return Selector(text=response_)  # 得到破解后的新response



