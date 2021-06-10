import os
import pandas as pd
import scrapy
from selenium import webdriver
from ..items import SpiderZhihuItem


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    middle_control = '登录'
    file_path = os.path.dirname(__file__)
    spider_title = [] # 读取repeat.txt得到的title
    url_title = [] # 在爬取过程中的title

    def __init__(self):
        # 让网页不加载图片
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.set_page_load_timeout(30)

        # 获取重复的title
        store_file = os.path.dirname(__file__) + '/repeat.txt'
        f = open(store_file, encoding='utf-8')
        for i in f.read().split('||'):
            self.spider_title.append(i)


    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        url = 'https://www.zhihu.com/topic/19864829/hot'
        yield scrapy.Request(url=url, callback=self.parse_1)
        self.middle_control = '一级'
        self.repeat = ''
        url = 'https://www.zhihu.com/topic/19864829/top-answers'
        yield scrapy.Request(url=url, callback=self.parse_1)

    def parse_1(self, response):
        title_list = response.xpath("//div[@class='List-item TopicFeedItem']//h2[@class='ContentItem-title']//a//text()").extract()
        url_list = response.xpath("//div[@class='List-item TopicFeedItem']//h2[@class='ContentItem-title']//a/@href").extract()
        source_list = response.xpath(
            "//div[@class='List-item TopicFeedItem']//div[@class='AuthorInfo-head']//span[@class='UserLink AuthorInfo-name']//text()").extract()
        self.middle_control = '二级'
        for i in range(len(title_list)):
            title = title_list[i]
            url = 'https:' + url_list[i]
            source = source_list[i]
            item = SpiderZhihuItem(title=title, url=url, source=source)
            self.spider_title.append(title)
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_detail)
            print('二级页面爬取完毕')

    def parse_detail(self, response):
        item = response.meta['item']
        self.spider_title.append(item['title'])
        total_detail = ''
        detail_1 = response.xpath("//meta[@itemprop='keywords']/@content").extract()
        for i in detail_1:
            total_detail += i + '||'
        detail_2 = response.xpath("//meta[@name='keywords']/@content").extract()
        for i in detail_2:
            total_detail += i + '||'
        detail_3 = response.xpath("//div[@class='QuestionRichText QuestionRichText--expandable QuestionRichText--collapsed']//text()").extract()
        for i in detail_3:
            total_detail += i + '||'
        item['detail'] = total_detail
        answer = ''
        answer_list_1 = response.xpath("//span[@class='RichText ztext CopyrightRichText-richText']//p//text()").extract()
        answer_list_2 = response.xpath("//div[@class='RichText ztext CopyrightRichText-richText']//p//text()").extract()
        answer_list_3 = response.xpath("//div[@class='RichText ztext Post-RichText']//p//text()").extract()
        for i in answer_list_1:
            answer += '||' + i
        for i in answer_list_2:
            answer += '||' + i
        for i in answer_list_3:
            answer += '||' + i
        item['answer'] = answer
        yield item


