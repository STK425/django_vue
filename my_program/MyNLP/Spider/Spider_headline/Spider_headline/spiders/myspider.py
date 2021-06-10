import scrapy
from selenium import webdriver
from ..items import SpiderHeadlineItem
import os
import pandas as pd

class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    middle_control = '一级'
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
        # 让网页不加载图片
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.set_page_load_timeout(30)

        # 获取重复的url
        store_file = os.path.dirname(__file__) + '/repeat.txt'
        f = open(store_file, encoding='utf-8')
        for i in f.read().split('||'):
            self.spider_url.append(i)

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        url = 'https://www.toutiao.com/search/?keyword=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title_list = []
        for each in response.xpath("//div[@class='sections']//div[@class='articleCard']"):
            title = each.xpath("div[@class='item']//span[@class='J_title']//text()").extract()
            whole_title = ''
            for i in title:
                whole_title = whole_title + i.strip(' ')
            title_list.append(whole_title)
        ex_href = 'https://www.toutiao.com'
        url_list = response.xpath("//div[@class='sections']//div[@class='articleCard']//a[@class='link title']/@href").extract()
        source_list = response.xpath(
            "//div[@class='sections']//div[@class='articleCard']//div[@class='y-box footer']//a[@class='lbtn source J_source']//text()").extract()
        timestamp_list = response.xpath(
            "//div[@class='sections']//div[@class='articleCard']//div[@class='y-box footer']//span[@class='lbtn']//text()").extract()
        for i in range(len(title_list)):
            self.middle_control = '二级'
            title = title_list[i]
            url = ex_href + url_list[i]
            source = source_list[i]
            timestamp = timestamp_list[i]
            item = SpiderHeadlineItem(title=title, url=url, source=source, timestamp=timestamp)
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_detail)

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
        temp = ''
        for each in response.xpath("//title"):
            temp = '山东大学'
        total_message += temp
        item['detail'] = total_message
        yield item
