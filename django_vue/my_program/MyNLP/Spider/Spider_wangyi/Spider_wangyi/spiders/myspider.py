import scrapy
import pandas as pd
from ..items import SpiderWangyiItem
import os


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    # allowed_domains = ['163.com']
    start_urls = ['https://cn.bing.com/search?q=%e5%b1%b1%e4%b8%9c%e5%a4%a7%e5%ad%a6+site%3anews.163.com&first=1&FORM=PERE1']
    url = 'https://cn.bing.com/search?q=%e5%b1%b1%e4%b8%9c%e5%a4%a7%e5%ad%a6+site%3anews.163.com&first={}&FORM=PERE1'
    page = 1
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
        # 获取标题
        title_list = []
        for each in response.xpath("//li[@class='b_algo']//h2"):
            title = each.xpath("a//text()").extract()
            whole_title = ''
            for i in title:
                whole_title = whole_title + i.strip(' ')
            title_list.append(whole_title)
        # 获取每个标题对应的url
        url_list = response.xpath("//li[@class='b_algo']//h2//a/@href").extract()
        # 获取新闻来源-网易新闻
        source = '网易新闻'
        # 获取新闻的时间戳
        timestamp_list = [] # response.xpath("//li[@class='b_algo']//div[@class='b_caption']//p//text()").extract()
        for each in response.xpath("//li[@class='b_algo']//div[@class='b_caption']"):
            timestamp = each.xpath("p//text()").extract()
            whole_timestamp = ''
            for i in timestamp:
                whole_timestamp = whole_timestamp + i.strip(' ')
            timestamp_list.append(whole_timestamp)

        for i in range(len(timestamp_list)):
            temp_title = title_list[i]
            temp_time = timestamp_list[i]
            if '山东大学' in temp_title or '山大' in temp_title or '山东大学' in temp_time or '山大' in temp_time:
                title = temp_title
                url = url_list[i]
                source = source
                timestamp = temp_time
                item = SpiderWangyiItem(title=title, url=url, source=source, timestamp=timestamp)
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_detail)
                print('二级页面爬取完毕')

        print('{}页一级页面爬取完毕'.format(self.page))

        if self.page < 686:
            if self.page == 1:
                url = self.url.format(6)
                self.page = 6;
                yield scrapy.Request(url=url, callback=self.parse)
            else:
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
