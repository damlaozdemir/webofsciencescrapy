# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from webofscience.items import WebofscienceItem
from scrapy import Request
class Webofscience(scrapy.Spider):
    name = "webofscience"
    allowed_domains = ["apps.webofknowledge.com"]
    start_urls = [
	   "https://apps.webofknowledge.com/Search.do?product=UA&SID=Z2mm29XJBAeV6Ym7xMg&search_mode=GeneralSearch&prID=337bfdd0-8183-4151-a1be-7d955aba7783"
	]

    def matchadresses(self, myNumsList = [],myAddressList = []):
        #nums = [1,[2,3],[1,3]]

        #addresses = ["[ 1 ] Izmir Inst Technol, Dept Elect & Elect Engn, Izmir, Turkey", "[ 2 ] Gebze Tech Univ, Dept Comp Engn, Gebze, Turkey","[ 3 ] Abant Izzet Baysal Univ, Dept Elect & Elect Engn, Bolu, Turkey"]
        matchedaddress=[]

        for num in myNumsList:

                if(isinstance(num, list)):
                    subarray=[]
                    for n in num:
                        for address in myAddressList:
                            if(n==int(address[2:3])):
                                subarray.append(address)

                            else:
                                continue
                    matchedaddress.append(subarray)

                else:
                    for address in myAddressList:
                        if(num == int(address[2:3])):
                            matchedaddress.append(address)
                        else:
                            continue
        return matchedaddress


    def parse(self, response):
        next_page = response.xpath("//a[@class='paginationNext']/@href").extract()
        if not not next_page:
            yield Request(next_page[0], self.parse)

        links = response.xpath("//a[@class='smallV110']/@href").extract()
        for link in links:
            link = "https://apps.webofknowledge.com" + link
            request = scrapy.Request(link,callback=self.parse_page2)
            yield request



    def parse_page2(self, response):
        item= WebofscienceItem()
        item['title'] =  response.xpath("//div[@class='title']/value/text()").extract()
        item['abstract'] = response.xpath("//div[contains(text(), 'Abstract')]/following-sibling::p/text()").extract()
        item['address'] = response.xpath("//td[@class='fr_address_row2']/a/text()").extract()
        item['keywords'] = response.xpath("//a[@title='Find more records by this author keywords']/text()").extract()
        item['keywordsplus'] = response.xpath("//a[@title='Find more records by this keywords plus']/text()").extract()
        item['authors'] = response.xpath("//a[@title='Find more records by this author']/text()").extract()
        item['journal'] = response.xpath("//p[@class='sourceTitle']/value/text()").extract()
        item['DOI'] = response.xpath("//span[contains(text(), 'DOI')]/following-sibling::value/text()").extract()
        item['published'] = response.xpath("//span[contains(text(), 'Published')]/following-sibling::value/text()").extract()
        mainresearcharea = response.xpath("//span[contains(text(), 'Research Areas')]/following-sibling::span/text()").extract()
        subresearcharea = response.xpath("//span[contains(text(), 'Research Areas')]/following-sibling::text()").extract()
        for m in mainresearcharea:
            for s in subresearcharea:
                item['researchareas'] = m + s

        item['webofsciencecategories'] = response.xpath("//span[contains(text(), 'Web of Science Categories')]/following-sibling::text()").extract()
        addressnum= response.xpath("//sup/b//text()").extract()
        address=[]
        for addnum in addressnum:

            a1 = addnum.strip()
            #a1= [w.replace(']', ';') for w in a1]
            address.append(a1)

        item['addressnumbers'] =address
        #for anum in addressnum:
        #    for address in addresses:
        #        item['address'] = self.matchadresses(anum, address)
        yield item
