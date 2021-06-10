import scrapy
from ..items import SpiderCctvItem
import os


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://search.cctv.com/search.php?qtext=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&sort=relevance&type=web&vtime=&datepid=1&channel=&page=1']
    url = 'https://search.cctv.com/search.php?qtext=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&sort=relevance&type=web&vtime=&datepid=1&channel=&page={}'
    page = 1
    # 重复的url
    spider_url = []

    def __init__(self):
        # 获取重复的url
        store_file = os.path.dirname(__file__) + '/repeat.txt'
        f = open(store_file, encoding='utf-8')
        for i in f.read().split('||'):
            self.spider_url.append(i)

    def parse(self, response):
        title_list = []
        # for each 下面的循环寻找的是下一级的标签，如果下一标签没有不会到第二级下面寻找
        for each in response.xpath("//div[@class='outer']//li"):
            title1 = each.xpath("h3[@class='tit']//a//text()").extract()
            title2 = each.xpath("div[@class='tright']//h3[@class='tit']//a//text()").extract()
            title = title1 + title2
            whole_title = ''
            for i in title:
                whole_title = whole_title + i.strip(' ')
            title_list.append(whole_title)
        # title_list = response.xpath("//div[@class='outer']//li//h3[@class='tit']//a/text()").extract()
        title_detail_list = []
        for each in response.xpath("//div[@class='outer']//li"):
            title_detail1 = each.xpath("p[@class='bre']//text()").extract()
            title_detail2 = each.xpath("div[@class='tright']//p[@class='bre']//text()").extract()
            title_detail = title_detail1 + title_detail2
            whole_title_detail = ''
            for i in title_detail:
                whole_title_detail = whole_title_detail + i.strip(' ')
            title_detail_list.append(whole_title_detail)
        url_list = response.xpath("//div[@class='outer']//li//h3[@class='tit']//span/@lanmu1").extract()
        source = '央视网'
        timestamp_list = response.xpath("//div[@class='outer']//li//span[@class='tim']/text()").extract()
        for i in range(len(title_list)):
            if title_list[i].find('山东大学')>-1 or title_list[i].find('山大')>-1 or title_detail_list[i].find('山东大学')>-1 or title_detail_list[i].find('山大')>-1:
                title = title_list[i]
                url = url_list[i]
                timestamp = timestamp_list[i]
                item = SpiderCctvItem(title=title, url=url, source=source, timestamp=timestamp)
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_detail)
                print('二级页面爬取完毕')

        print('{}页一级页面爬取完毕'.format(self.page))

        if self.page < 30:
            self.page += 1;
            url = self.url.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        total_message = ''
        for each in response.xpath("//a"):
            total_message = '山东大学.'
        for each in response.xpath("//ul[@class='ul1-1']//li//a"):
            message = each.xpath("text()").extract()
            total_message = total_message + message[0].replace(' ', '') + '.'
        item['detail'] = total_message
        yield item