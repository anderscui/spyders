import re
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from cnblogs.items import CnblogsItem
from scrapy.http import Request, Response


class CnblogsSpider(BaseSpider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['http://www.cnblogs.com/']

    crawledLinks = []

    def get_url_of_page(self, page):
        return 'http://www.cnblogs.com/sitehome/p/{0}'.format(page)

    def parse(self, response):

        more_pages = [self.get_url_of_page(p) for p in xrange(2, 6)]
        for page_url in more_pages:
            CnblogsSpider.crawledLinks.append(page_url)
            yield Request(page_url, self.parse_more_page)

        posts = response.xpath('//div[@class="post_item_body"]')
        print posts
        for post in posts:
            item = CnblogsItem()
            item['title'] = post.xpath('h3/a/text()').extract()
            item['summary'] = post.xpath('p[@class="post_item_summary"]/text()').extract()
            yield item

    def parse_more_page(self, response):

        posts = response.xpath('//div[@class="post_item_body"]')

        for post in posts:
            item = CnblogsItem()
            item['title'] = post.xpath('h3/a/text()').extract()
            item['summary'] = post.xpath('p[@class="post_item_summary"]/text()').extract()
            yield item