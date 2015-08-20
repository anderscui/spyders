# -*- coding: utf-8 -*-

from scrapy import Item, Field


class KeywordItem(Item):
    id = Field()
    name = Field()
    category = Field()
    subcategory = Field()
    encoded = Field()
    created_on = Field()
    updated_on = Field()


class PositionItem(Item):
    # 'leaderName=暂没有填写'
    # null

    # meta
    id = Field()
    pos_id = Field()
    name = Field()
    create_time = Field()
    city = Field()
    salary = Field()
    time_type = Field()
    fin_stage = Field()
    industry = Field()

    category = Field()
    subcategory = Field()

    # contents
    desc = Field()

    # extended
    leader = Field()
    advantage = Field()

    # requirements
    education = Field()
    experience = Field()

    # company
    com_id = Field()
    com_name = Field()
    com_short_name = Field()
    com_url = Field()
    com_labels = Field()
    com_logo = Field()
    com_size = Field()
    com_address = Field()

    # tracking
    created_on = Field()
    updated_on = Field()