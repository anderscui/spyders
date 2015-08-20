# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from lagou.items import KeywordItem, PositionItem


class LagouPipeline(object):
    def process_item(self, item, spider):
        return item


class PositionsSQLitePipeline(object):
    filename = 'lagou.db'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, domain):

        if isinstance(item, PositionItem):
            # print item['pos_id']
            try:

                if (not item['desc']) or (item['desc'] == 'n/a'):

                    # create a new position
                    self.conn.execute("""insert into position(pos_id, name, create_time, city, salary, time_type, fin_stage, industry,
                                         category, subcategory, desc, leader, advantage, education, experience,
                                         com_id, com_name, com_short_name, com_url, com_labels, com_logo, com_size, com_address,
                                         created_on, updated_on) values (?, ?, ?, ?, ?, ?, ?, ?,
                                                                         ?, ?, ?, ?, ?, ?, ?,
                                                                         ?, ?, ?, ?, ?, ?, ?, ?,
                                                                         ?, ?)""",
                                      (item['pos_id'], item['name'], item['create_time'], item['city'], item['salary'], item['time_type'], item['fin_stage'], item['industry'],
                                       item['category'], item['subcategory'], item['desc'], item['leader'], item['advantage'], item['education'], item['experience'],
                                       item['com_id'], item['com_name'], item['com_short_name'], item['com_url'], item['com_labels'], item['com_logo'], item['com_size'], item['com_address'],
                                       item['created_on'], item['updated_on']))

                else:
                    # update an existing position
                    self.conn.execute("""update position set desc = ?, com_url = ?, com_address = ? where pos_id = ?""",
                                    (item['desc'], item['com_url'], item['com_address'], item['pos_id']))

            except sqlite3.Error, e:
                print 'Failed to insert item: ' + str(item['pos_id']) + " --> " + e.args[0]
        elif isinstance(item, KeywordItem):
            try:
                self.conn.execute('insert into keyword(name, category, subcategory, encoded, created_on, updated_on) values (?, ?, ?, ?, ?, ?)',
                                  (item['name'], item['category'], item['subcategory'],
                                   item['encoded'], item['created_on'], item['updated_on']))
            except sqlite3.Error, e:
                print 'Failed to insert item: ' + item['name'] + " --> " + e.args[0]
        else:
            print "Sorry, I don't know you:("

        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""not real sql""")
        conn.commit()
        return conn