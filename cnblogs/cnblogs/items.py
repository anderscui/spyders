# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class CnblogsItem(Item):
    title = Field()
    summary = Field()