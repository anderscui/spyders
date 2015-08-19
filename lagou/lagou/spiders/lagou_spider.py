import scrapy

from lagou.items import PositionItem


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = [
        "http://www.lagou.com/",
    ]

    def parse(self, response):
        self.logger.info('parse function called on %s', response.url)

        return scrapy.FormRequest(url='http://www.lagou.com/jobs/positionAjax.json?',
                                  formdata={'first': 'false', 'pn': '1', 'kd': 'Python'},
                                  callback=self.parse_job_list)

    def parse_job_list(self, response):
        self.logger.info('parsing contents of dir - %s', response.url)

        item = PositionItem()
        item['title'] = 'test'
        yield item
