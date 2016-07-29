# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebofscienceItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()
    keywordsplus = scrapy.Field()
    address = scrapy.Field()
    journal = scrapy.Field()
    DOI = scrapy.Field()
    published = scrapy.Field()
    researchareas = scrapy.Field()
    webofsciencecategories = scrapy.Field()
    addressnumbers=scrapy.Field()
    pass
