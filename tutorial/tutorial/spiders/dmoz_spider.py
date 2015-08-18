import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['dmoz.org']
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()

            t = sel.xpath('a/text()').extract()
            l = sel.xpath('a/@href').extract()
            d = sel.xpath('text()').extract()

            if len(t) == 0 or len(l) == 0 or len(d) == 0:
                print('incomplete data........')

            item['title'] = t[0] if t else 'N/A'
            item['link'] = l[0] if l else 'N/A'
            item['desc'] = d[-1] if d else 'N/A'
            yield item


