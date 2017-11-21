# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapySearchRankingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Category = scrapy.Field()
    SubCat = scrapy.Field()
    SubSubCat = scrapy.Field()
    ProductName = scrapy.Field()
    SuggPrice = scrapy.Field()
    BoardType = scrapy.Field()




