import os
from ..items import SpiderWeiboItem
import scrapy
from selenium import webdriver


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    middle_control = '登录'
    file_path = os.path.dirname(__file__)
    spider_url = []  # 读取repeat.txt得到的url

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
        url = 'https://s.weibo.com/topic?q=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&pagetype=topic&topic=1&Refer=article_topic&page={}'
        yield scrapy.Request(url=url.format(1), callback=self.parse)
        self.middle_control = '一级'
        for i in range(8):
            yield scrapy.Request(url=url.format(i + 2), callback=self.parse)

    def parse(self, response):
        title_list = response.xpath(
            "//div[@class='card card-direct-a s-mb20']//div[@class='info']//a[@class='name']/text()").extract()
        url_list = response.xpath(
            "//div[@class='card card-direct-a s-mb20']//div[@class='info']//a[@class='name']/@href").extract()
        detail_list = []
        for each in response.xpath("//div[@class='card card-direct-a s-mb20']//div[@class='info']"):
            detail = each.xpath("p//text()").extract()
            whole_detail = ''
            for i in detail:
                whole_detail += i
            detail_list.append(whole_detail)
        self.middle_control = '一级'
        for i in range(len(title_list)):
            title = title_list[i]
            url = url_list[i]
            detail = detail_list[i]
            item = SpiderWeiboItem(title=title, url=url, detail=detail)
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_detail_1)
            print('二级页面爬取完毕')

    def parse_detail_1(self, response):
        item = response.meta['item']
        page_exist = 0
        for each in response.xpath("//ul[@class='s-scroll']//li"):
            page_exist += 1
            url = 'https://s.weibo.com' + each.xpath("a/@href").extract()[0]
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_detail_2)
        if page_exist == 0:
            yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parse_detail_2)

    def parse_detail_2(self, response):
        item = response.meta['item']
        content_list = response.xpath(
            "//div[@action-type='feed_list_item']//p[@node-type='feed_list_content']//text()").extract()
        time_list = response.xpath("//div[@action-type='feed_list_item']//p[@class='from']//text()").extract()
        whole_content = ''
        whole_time = ''
        for each in content_list:
            whole_content += each
        for each in time_list:
            whole_time += each
        item['content'] = whole_content
        item['timestamp'] = whole_time
        yield item
