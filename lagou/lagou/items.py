# -*- coding: utf-8 -*-

from scrapy import Item, Field
import sqlite3


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
    is_active = Field()

    tag = Field()
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

    # modes
    # new, brief, detail
    mode = Field()

    # tracking
    created_on = Field()
    updated_on = Field()


class ItemDao(object):
    dbfile = 'lagou.db'

    def keyword_exists(self, keyword):
        conn = sqlite3.connect(self.dbfile)
        with conn:
            cur = conn.cursor()
            val = cur.execute('SELECT EXISTS(SELECT 1 FROM keyword WHERE name = ?)', (keyword,)).fetchone()[0]
            return val

    def pos_exists(self, pos_id):
        conn = sqlite3.connect(self.dbfile)
        with conn:
            cur = conn.cursor()
            val = cur.execute('SELECT EXISTS(SELECT 1 FROM position WHERE pos_id = ?)', (pos_id,)).fetchone()[0]
            return val

    def get_keywords(self):

        conn = sqlite3.connect(self.dbfile)
        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT name FROM keyword')
            rows = cur.fetchall()
            return [row['name'] for row in rows]

    # select  pos_id, desc, updated_on from position where pos_id = 783265
    def pos_desc_exists(self, pos_id):
        conn = sqlite3.connect(self.dbfile)
        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            row = cur.execute('select pos_id, desc, create_time, tag, updated_on from position where pos_id = ?', (pos_id,)).fetchone()

            row_exists, desc_exists, create_time, tag = False, False, None, None
            if row:
                row_exists = True

                desc = row['desc']
                create_time = row['create_time']
                tag = row['tag']

                if desc != 'n/a':
                    desc_exists = True

            return row_exists, desc_exists, create_time, tag