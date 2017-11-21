# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


class LoadPageMiddleware(object):
    #

    def process_request(self,request,spider):
        driver = webdriver.PhantomJS()
        driver.get(request.url)
        driver.implicitly_wait(3)
        time.sleep(4)

        current_subcat = request.meta.get('subcat',-1)
        current_subsubcat = request.meta.get('subsubcat',-1)
        if  (current_subcat != -1) and current_subsubcat == -1:
            driver.find_element_by_xpath(u'//h4/span[@class="nav-title" and text()="%s"]/parent::*/parent::*/following-sibling::div[@class="block-tail"]'%(current_subcat)).click()
            # driver.find_element_by_xpath(u'//h4/span[@class="nav-title"]').click()
            driver.implicitly_wait(2)

        if request.meta.get('type_flag',False):
            driver.find_element_by_xpath(u'//div[@class="col switch-item "]/a[text()="销售热门排行"]').click()
            driver.implicitly_wait(2)
            request.meta.update({'type_flag':False})

        true_page = driver.page_source
        driver.close()

        return HtmlResponse(request.url,body=true_page, encoding='utf-8', request=request)




class ScrapySearchRankingSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
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
