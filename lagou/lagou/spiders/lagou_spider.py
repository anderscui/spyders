# coding=utf-8

import datetime
import json
import scrapy

from lagou.items import KeywordItem, PositionItem, ItemDao
from scrapy.exceptions import CloseSpider


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = [
        "http://www.lagou.com/",
    ]

    pos_list_url_format = u'http://www.lagou.com/jobs/positionAjax.json?kd={0}&pn={1}&first=false'
    pos_detail_url_format = u'http://www.lagou.com/jobs/{0}.html'

    get_pos_detail = True

    def parse(self, response):
        self.logger.info('parse function called on %s', response.url)

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

        item_dao = ItemDao()
        kd = item_dao.get_keywords()
        # kd = [u'搜索算法', u'精准推荐']
        # kd = [u'Python', u'自然语言处理']
        pos_urls = [(k, self.pos_list_url_format.format(k, 1)) for k in kd]

        if get_positions:
            for pu in pos_urls:
                request = scrapy.Request(url=pu[1], callback=self.parse_pos_list)
                request.meta['kd'] = pu[0]
                request.meta['pn'] = 1
                yield request

    def parse_pos_list(self, response):
        if response.status != 200:
            raise CloseSpider('response status code: {0}, url: {1}'.format(response.status, response.url))

        result = json.loads(response.body)
        if not result['success']:
            raise CloseSpider('fetch pos list failed, url: {0}'.format(response.url))

        print 'pos_list', response.url
        # print 'body', response.body
        kd = response.meta['kd']
        print kd

        if result and result['content'] and result['content']['result']:

            for pos in result['content']['result']:
                item = PositionItem()
                item["pos_id"] = int(pos["positionId"])

                item_dao = ItemDao()
                pos_exists, desc_exists, create_time, tag = item_dao.pos_desc_exists(item["pos_id"])

                # new, brief, detail

                if pos_exists:
                    print('update brief of {0}'.format(item["pos_id"]))

                    item["mode"] = "brief"
                    item["create_time"] = pos["createTime"]
                    if not tag:
                        tag = kd
                    else:
                        tags = unicode(tag).split(',')
                        if kd not in tags:
                            tags.append(kd)
                        tag = ','.join(tags)
                    item['tag'] = tag
                    item['updated_on'] = datetime.datetime.now()

                else:
                    item["mode"] = "new"
                    item['tag'] = kd

                    item["name"] = pos["positionName"]
                    item["create_time"] = pos["createTime"]
                    item["city"] = pos["city"]
                    item["salary"] = pos["salary"]
                    item["time_type"] = pos["jobNature"]
                    item["fin_stage"] = pos["financeStage"]
                    item["industry"] = pos["industryField"]
                    item["is_active"] = 1

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

                # pos detail
                if not desc_exists and self.get_pos_detail:
                    yield scrapy.Request(url=self.pos_detail_url_format.format(item["pos_id"]),
                                         callback=self.parse_pos_detail)

        else:
            print 'invalid result'

        # next page
        c = result['content']
        cur_page = int(response.meta['pn'])
        total_pages = int(c['totalPageCount'])
        print 'pager: %d of %d' % (cur_page, total_pages)
        if cur_page < total_pages:
            kd = response.meta['kd']
            request = scrapy.Request(url=self.pos_list_url_format.format(kd, (cur_page+1)), callback=self.parse_pos_list)
            print 'next url: ', request.url
            request.meta['kd'] = kd
            request.meta['pn'] = cur_page + 1
            yield request

    def parse_pos_detail(self, response):
        if response.status != 200:
            raise CloseSpider('response status code: {0}, url: {1}'.format(response.status, response.url))

        pos_id = response.xpath("//input[@id='jobid']/@value").extract()[0]
        pos_desc = response.xpath("//dd[@class='job_bt']").extract()[0]

        company = response.xpath("//dl[@class='job_company']")
        com_url = company.re(u"<span>主页</span>\s*<a href=\"(.+?)\".+</a>")
        com_address = company.re(u"<h4>工作地址</h4>\s*<div>(?P<address>.+)</div>")

        item = PositionItem()
        item["mode"] = "detail"
        item["pos_id"] = int(pos_id)
        item["desc"] = pos_desc
        item["com_url"] = com_url[0] if com_url else 'n/a'
        item["com_address"] = com_address[0] if com_address else 'n/a'
        item['updated_on'] = datetime.datetime.now()

        yield item

