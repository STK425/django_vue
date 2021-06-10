# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random
import time, os
from time import sleep
from scrapy import signals
import pandas as pd

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from .settings import  USER_AGENT_LIST

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        rand_use = random.choice(USER_AGENT_LIST)
        if rand_use:
            request.headers.setdefault('User-Agent', rand_use)


class SpiderZhihuSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderZhihuDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 根据txt的内容来判重
        repeat = spider.spider_title[len(spider.spider_title)-1]
        del spider.spider_title[len(spider.spider_title)-1]
        if spider.middle_control == '二级' and repeat != '' and repeat in spider.spider_title:
            return HtmlResponse(url=spider.browser.current_url, body=None,
                                encoding="utf-8", request=request)

        if spider.middle_control == '登录':
            LOGIN_URL = 'https://www.zhihu.com/'
            spider.browser.get(LOGIN_URL)
            time.sleep(2)
            # 下面的文件位置需要自己改，与上面的改动一致
            f = open(spider.file_path + '/zhihu.txt')
            cookies = f.read()
            jsonCookies = json.loads(cookies)
            for co in jsonCookies:
                spider.browser.add_cookie(co)
            spider.browser.refresh()
            time.sleep(2)
            spider.browser.get(request.url)
            sleep(2)
            try:
                for i in range(10):
                    spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    sleep(2)
            except TimeoutException as e:
                print('超时')
                spider.browser.execute_script('window.stop()')
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                encoding="utf-8", request=request)
        if spider.middle_control == '一级':
            try:
                spider.browser.get(request.url)
                for i in range(30):
                    spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    sleep(2)
            except TimeoutException as e:
                print('超时')
                spider.browser.execute_script('window.stop()')
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                encoding="utf-8", request=request)
        if spider.middle_control == '二级':
            answer_num = 1
            try:
                spider.browser.get(request.url)
            except TimeoutException as e:
                print('超时')
                spider.browser.execute_script('window.stop()')
            try:
                answer_num = spider.browser.find_element_by_xpath(
                    "//a[@class='QuestionMainAction ViewAll-QuestionMainAction']").text
                spider.browser.find_element_by_xpath(
                    "//a[@class='QuestionMainAction ViewAll-QuestionMainAction']").click()
                answer_num = int(int(answer_num.strip('查看全部  个回答'))/5)
                sleep(1)
                if answer_num >= 30:
                    answer_num = 30
            except:
                pass
            for i in range(answer_num):
                spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                encoding="utf-8", request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
