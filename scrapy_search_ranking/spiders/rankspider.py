# -*- coding: utf-8 -*-
import scrapy
from scrapy_search_ranking.items import ScrapySearchRankingItem
import re

class TaobaoRankSpider(scrapy.Spider):

    name = 'rankspider'

    start_urls = ["https://top.taobao.com/index.php?topId=TR_FS&leafId=50010850"]

    def start_requests(self):
        return [scrapy.Request('https://top.taobao.com/index.php?spm=a1z5i.1.2.1.hUTg2J&topId=HOME', callback=self.cat_parser)]

    def cat_parser(self,response):
        all_tabs = response.xpath('//li[@class="tab"]/a')
        for tab in all_tabs[1:2]:
            url = 'https:' + tab.xpath('./@href').extract_first()
            category = tab.xpath('./text()').extract_first()
            meta = {'category':category}
            yield scrapy.Request(url, callback=self.subcat_parser_step1, meta=meta)

    def subcat_parser_step1(self,response):
        meta = response.meta
        subcats = response.xpath('//h4/span[@class="nav-title"]/text()').extract()
        for subcat in subcats[:1]:
            meta.update({'subcat':subcat})
            yield scrapy.Request(response.url, callback=self.subcat_parser_step2, meta=meta, dont_filter=True)

    def subcat_parser_step2(self,response):
        meta = response.meta
        current_subcat = meta['subcat']
        print current_subcat
        subcat = response.xpath('//div[@class="J_Row nav-block J_commonBlock type- block-expand"]')
        subcat_name = subcat.xpath('.//span[@class="nav-title"]/text()').extract_first()
        assert(subcat_name == current_subcat)
        subsubcats = subcat.xpath('.//a[@target="_self"]')
        for subsubcat in subsubcats[:1]:
            url = "https://top.taobao.com/{}".format(subsubcat.xpath('./@href').extract_first()[1:])
            subsubcat_name = subsubcat.xpath('./text()').extract_first()
            meta.update({'subsubcat':subsubcat_name,'type':'rising'})
            yield scrapy.Request(url, callback=self.parse, meta=meta, dont_filter=True)
            meta.update({'subsubcat':subsubcat_name,'type':'hot','type_flag':True})
            yield scrapy.Request(url, callback=self.parse, meta=meta, dont_filter=True)

    def parse(self,response):
        all_rows = response.xpath('//li[@class="content-row J_contentRow"]')
        for row in all_rows:
            item = ScrapySearchRankingItem()
            item['ProductName'] = row.xpath('.//div[@class="col2 col"]//a[@target="_blank"]/text()').extract_first()
            item['SuggPrice'] = re.search('[0-9]+[\.,0-9]*',row.xpath('.//div[@class="col3 col"]/text()').extract_first()).group(0)
            item['Category'] = response.meta['category']
            item['SubCat'] = response.meta['subcat']
            item['SubSubCat'] = response.meta['subsubcat']
            item['BoardType'] = response.meta['type']
            yield item
        try:
            next_page = "https://top.taobao.com/{}".format(response.xpath('//li[@class="item next"]/a/@href').extract_first())
            yield scrapy.Request(next_page, callback=self.parse, meta=response.meta)
            print 'next page found'
        except:
            print 'no next page'

