# [Crawler_58City](https://github.com/sggs7654/Crawler_58City)

解析58同城中全国城市的房屋出租信息页面，抓取房屋出租数据，清洗并持久化至本地Redis数据库中

主要特点：1）应对字体反爬 2）UA伪造 3）应对IP封锁 4) Scrapy中间件及Item pipline

抓取流程
---
1. 访问58同城城市切换页面，解析各城市分支url
2. 访问各城市房屋出租列表页，抓取房屋出租信息

环境依赖
---

Scrapy / requests / redis-py / Xpath / regex

使用须知
---
本代码仅作学习交流，切勿用于商业用途，否则后果自负。若涉及58侵权，请邮箱联系，会尽快处理。
