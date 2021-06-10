# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderZhihuItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    # detail里面包含相关话题以及简介
    detail = scrapy.Field()
    # 回答之间用||分开
    answer = scrapy.Field()
