import scrapy
import os
import pandas as pd
from ..items import SpiderSinaItem
from selenium import webdriver


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    # 网页page从1开始一直到50
    url = 'https://search.sina.com.cn/?q=%e5%b1%b1%e4%b8%9c%e5%a4%a7%e5%ad%a6&c=news&from=&col=&range=all&source' \
          '=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page={}'
    page = 0
    middle_control = '登录'
    file_path = os.path.dirname(__file__)
    stop_words = []
    # 文件的位置
    store_file = os.path.dirname(__file__) + '/IrrelevantWords.txt'
    data = pd.read_csv(store_file, header=None, sep=".")
    for i in range(data.shape[1]):
        if data[i][0] not in stop_words:
            stop_words.append(data[i][0])
    # 重复的url
    spider_url = []

    '''def start_requests(self):  # 重构start_requests方法
        # 这个cookies_str是抓包获取的
        cookies_str = 'SINAGLOBAL=222.175.103.101_1540095202.97534; U_TRS1=000000a0.2eb3f6f.5da12a27.95d401d2; gr_user_id=bad2ea7a-0a89-4e23-b8de-5b9f103f9616; grwng_uid=81b45283-5624-4f6e-895e-429ab5d0675b; SGUID=1617706642726_99503363; UM_distinctid=178a6d475f02e6-0af51b5715f299-7166786d-144000-178a6d475f12f0; UOR=,,; _ga=GA1.3.550869381.1618969403; __gads=ID=90f2d5f97639af20-22a66d4383c70046:T=1618972035:RT=1618972035:S=ALNI_MbrJgpV5V-IsqldW_cH1-TrT313gw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh6S37JcPH26hK.i69ex_m85NHD95Qc1KMRSKq4e02cWs4DqcjPi--fi-i8iKn7i--NiK.NiK.fe0B7e02t; ALF=1653465070; Apache=124.128.225.204_1621929079.669865; U_TRS2=00000014.685b3292.60acac80.463161f1; ULV=1621930715643:10:4:3:124.128.225.204_1621929079.669865:1621913971884; _gid=GA1.3.777494417.1621938247; SEARCH-SINA-COM-CN=484fb5dd86ee7bffbce4d7b80076f126'  # 抓包获取
        # 将cookies_str转换为cookies_dict
        cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split('; ')}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies_dict
        )'''

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
        url = 'https://news.sina.com.cn/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.middle_control = '一级'
        title_list = []
        for each in response.xpath("//div[@class='box-result clearfix']//h2"):
            title = each.xpath("a//text()").extract()
            whole_title = ''
            for i in title:
                whole_title = whole_title + i.strip(' ')
            title_list.append(whole_title)
        source_list = []
        timestamp_list = []
        for each in response.xpath("//div[@class='box-result clearfix']//h2"):
            whole = each.xpath("span//text()").extract()
            time_source = whole[0].split()
            source_list.append(time_source[0])
            timestamp_list.append(time_source[1])
        url_list = response.xpath("//div[@class='box-result clearfix']//h2//a/@href").extract()
        for i in range(len(title_list)):
            title = title_list[i]
            url = url_list[i]
            source = source_list[i]
            timestamp = timestamp_list[i]
            item = SpiderSinaItem(title=title, url=url, source=source, timestamp=timestamp)
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_detail)
            print('二级页面爬取完毕')

        print('{}页一级页面爬取完毕'.format(self.page))

        if self.page <= 30:
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
