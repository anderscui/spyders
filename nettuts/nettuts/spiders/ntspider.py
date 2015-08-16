import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from nettuts.items import NettutsItem
from scrapy.http import Request


class NettutsSpider(BaseSpider):
    name = 'nettuts'
    allowed_domains = ['net.tutsplus.com']
    start_urls = ['http://net.tutsplus.com/']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select("//a/@href").extract()

        crawledLinks = []

        linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

        for link in links:
            if linkPattern.match(link) and not link in crawledLinks:
                crawledLinks.append(link)
                yield Request(link, self.parse)

        titles = hxs.select('//li[@class="posts__post"]/a/text()').extract()
        for title in titles:
            item = NettutsItem()
            item['title'] = title
            yield item