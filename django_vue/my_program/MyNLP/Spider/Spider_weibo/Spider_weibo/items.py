# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderWeiboItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    detail = scrapy.Field()
    content = scrapy.Field()
    pass
