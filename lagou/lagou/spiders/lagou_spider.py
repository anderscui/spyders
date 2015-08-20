import datetime
import json
import scrapy

from lagou.items import KeywordItem, PositionItem


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = [
        "http://www.lagou.com/",
    ]

    def parse(self, response):
        self.logger.info('parse function called on %s', response.url)
        self.pos_list_url_format = 'http://www.lagou.com/jobs/positionAjax.json?kd={0}&pn={1}&first=false'

        get_keywords = False
        get_positions = True
        position_limit = 20

        if get_keywords:

            cats = response.xpath("//div[@class='mainNavs']/div[@class='menu_box']")
            for cat in cats:
                cat_title = cat.xpath("div[@class='menu_main']/h2/text()").extract()
                category = ' '.join(cat_title).strip()

                sub_cats = cat.xpath("div/dl[@class='reset']")
                for sub_cat in sub_cats:
                    sub_title = ' '.join(sub_cat.xpath("dt/a/text()").extract()).strip()

                    positions = sub_cat.xpath("dd/a")
                    for pos in positions:
                        name = ' '.join(pos.xpath("text()").extract()).strip()
                        link = pos.xpath("@href").extract()[0]
                        query = link.split('/')[-1]

                        item = KeywordItem()
                        item['name'] = name
                        item['category'] = category
                        item['subcategory'] = sub_title
                        item['encoded'] = query
                        item['created_on'] = datetime.datetime.now()
                        item['updated_on'] = datetime.datetime.now()

                        yield item

        kd = ['Java', 'Python']
        pos_urls = [self.pos_list_url_format.format(k, i) for i in xrange(1, 3) for k in kd]

        if get_positions:
            for pu in pos_urls:
                yield scrapy.Request(url=pu, callback=self.parse_pos_list)

                # return scrapy.FormRequest(url='http://www.lagou.com/jobs/positionAjax.json?',
                # formdata={'first': 'false', 'pn': '1', 'kd': 'Python'},
                # callback=self.parse_job_list)

    def parse_pos_list(self, response):
        if response.status != 200:
            # self.close()
            yield None

        result = json.loads(response.body)
        if not result['success']:
            yield None

        for pos in result['content']['result']:
            item = PositionItem()
            item["pos_id"] = int(pos["positionId"])
            item["name"] = pos["positionName"]
            item["create_time"] = pos["createTime"]
            item["city"] = pos["city"]
            item["salary"] = pos["salary"]
            item["time_type"] = pos["jobNature"]
            item["fin_stage"] = pos["financeStage"]
            item["industry"] = pos["industryField"]

            item["category"] = pos["positionFirstType"]
            item["subcategory"] = pos["positionType"]

            # TODO:
            item["desc"] = 'n/a'

            item["leader"] = pos["leaderName"]
            item["advantage"] = pos["positionAdvantage"]

            item["education"] = pos["education"]
            item["experience"] = pos["workYear"]

            item["com_id"] = int(pos["companyId"])
            item["com_name"] = pos["companyShortName"]
            item["com_short_name"] = pos["companyName"]
            # TODO:
            item["com_url"] = 'n/a'
            item["com_labels"] = ';'.join(pos["companyLabelList"])
            item["com_logo"] = pos["companyLogo"]
            item["com_size"] = pos["companySize"]
            # TODO:
            item["com_address"] = 'n/a'

            item['created_on'] = datetime.datetime.now()
            item['updated_on'] = datetime.datetime.now()

            yield item