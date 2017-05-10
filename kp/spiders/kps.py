# -*- coding: utf-8 -*-
import scrapy
from kp.items import BookItem

class KpsSpider(scrapy.Spider):
    name = "kps"
    allowed_domains = ["kindlepush.com"]
    start_urls = (
            'http://kindlepush.com/category/-1/0/1',
    )
    def lessone(self,arr):
        if len(arr)>=1:
            return arr[-1]
        else:
            return ""

    def parse(self, response):
        bprev_url = 'http://kindlepush.com:80/book/'
        infos = response.css('.info .wrap')
        for info in infos:
            item = BookItem()
            item['book_url'] = info.css('.title').xpath('./@href').extract()[-1][len(bprev_url):]
            #print item['book_url']
            item['book_name'] = self.lessone(info.css('.title::text').extract())
            item['book_score'] = self.lessone(info.css('.num::text').extract())
            item['book_author'] = self.lessone(info.css('.u-author').xpath('span/text()').extract())
            yield item

        next_url = response.css('.u-page').xpath('./a/@href').extract()[-1]
        #print next_url
        yield scrapy.Request(url=next_url, callback=self.parse)
