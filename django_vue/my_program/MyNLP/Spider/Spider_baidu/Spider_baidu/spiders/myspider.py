import scrapy
from ..items import SpiderBaiduItem
import datetime
import pandas as pd
import os

class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    # allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_'
                  'pc&word=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&'
                  'tngroupname=organic_news&newVideo=12&pn=0']
    url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_'\
          'pc&word=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&'\
          'tngroupname=organic_news&newVideo=12&pn={}'
    page = 0
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
        for each in response.xpath("//div[@class='result-op c-container xpath-log new-pmd']//h3[@class='news-title_1YtI1']"):
            title = each.xpath("a//text()").extract()
            whole_title = ''
            for i in title:
                whole_title = whole_title + i.strip(' ')
            title_list.append(whole_title)
        url_list = response.xpath("//div[@class='result-op c-container xpath-log new-pmd']//h3//a/@href").extract()
        source_list = response.xpath("//div[@class='result-op c-container xpath-log new-pmd']//div[@class='news-source']//span[@class='c-color-gray c-font-normal c-gap-right']/text()").extract()
        timestamp_list = response.xpath("//div[@class='result-op c-container xpath-log new-pmd']//div[@class='news-source']//span[@class='c-color-gray2 c-font-normal']/text()").extract()
        for i in range(len(title_list)):
            title = title_list[i]
            url = url_list[i]
            source = source_list[i]
            timestamp = timestamp_list[i]
            if '小时前' in timestamp:
                timestamp = times
            item = SpiderBaiduItem(title=title, url=url, source=source, timestamp=timestamp)
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_detail)
            print('二级页面爬取完毕')

        print('{}页一级页面爬取完毕'.format(self.page))

        if self.page < 260:
            self.page += 10;
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
