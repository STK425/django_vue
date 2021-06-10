import scrapy
from scrapy.spiders import Spider
from ..items import SpiderIqiluItem
import datetime
import pandas as pd
import os

class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    # allowed_domains = ['iqilu.com']
    start_urls = ['http://s.iqilu.com/cse/search?q=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&p=0&s=2576961992730276856&nsid=1&entry=1']
    url = 'http://s.iqilu.com/cse/search?q=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&p={}&s=2576961992730276856&nsid=1&entry=1'
    page = 0
    #
    stop_words = []
    # 文件的位置
    store_file = os.path.dirname(__file__) + '/IrrelevantWords.txt'
    data = pd.read_csv(store_file, header=None, sep=".")
    for i in range(data.shape[1]):
        if data[i][0] not in stop_words:
            stop_words.append(data[i][0])
    # 重复的url
    spider_url = []

    def __init__(self):
        # 获取重复的url
        store_file = os.path.dirname(__file__) + '/repeat.txt'
        f = open(store_file, encoding='utf-8')
        for i in f.read().split('||'):
            self.spider_url.append(i)

    def parse(self, response):
        # 在一级界面中，获取网页上的标题，链接，来源，时间戳
        # items储存网页信息
        # print('当前网页的源码为: ' + response.body_as_unicode())
        # print(response.xpath("//div[@class='result-op c-container xpath-log new-pmd']//h3//a/text()"))
        current_time = datetime.datetime.now()
        times = '{}年{}月{}日'.format(current_time.year, current_time.month, current_time.day)
        title_list = []
        for each in response.xpath("//div[@class='result f s0']//h3[@class='c-title']"):
            title = each.xpath("a//text()").extract()
            whole_title = ''
            for i in title:
                whole_title = whole_title + i.strip(' ')
            title_list.append(whole_title)
        url_list = response.xpath("//div[@class='result f s0']//h3//a/@href").extract()
        timestamp_list = response.xpath("//div[@class='result f s0']//span[@class='c-showurl']/text()").extract()
        for i in range(len(title_list)):
            title = title_list[i]
            url = url_list[i]
            source = '齐鲁网'
            timestamp = timestamp_list[i]
            if '小时前' in timestamp:
                timestamp = times
            item = SpiderIqiluItem(title=title, url=url, source=source, timestamp=timestamp)
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_detail)
            print('二级页面爬取完毕')

        print('{}页一级页面爬取完毕'.format(self.page))

        if self.page < 75:
            self.page += 1;
            url = self.url.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_detail(self, response):
        item = response.meta['item']
        total_message = ''
        num = 0
        num_list = []
        for each in response.xpath("//a"):
            message = each.xpath("@href").extract()
            if len(message)!=0 and message[0]!='http://www.qq.com' and message[0]!='https://www.baidu.com':
                num_list.append(num)
            num += 1
        num = 0

        for each in response.xpath("//a"):
            message = each.xpath("text()").extract()
            if num in num_list:
                if len(message)!=0 and message[0].replace(' ', '') not in self.stop_words:
                    total_message = total_message + message[0].replace(' ', '') + '.'
            num += 1
        item['detail'] = total_message
        yield item
