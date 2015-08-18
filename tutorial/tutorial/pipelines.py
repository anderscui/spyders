# -*- coding: utf-8 -*-

import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class DmozPipeline(object):
    def process_item(self, item, spider):
        return item


class SQLiteStorePipeline(object):
    filename = 'dmoz.db'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, domain):
        try:
            self.conn.execute('insert into dmoz values(?, ?, ?)',
                              (item['title'], item['link'], item['desc']))
            # (item['title'], item['link'], item['desc'])
            # print item['title'][0], item['link'][0], item['desc'][0]
        except sqlite3.Error, e:
            print 'Failed to insert item: ' + item['title'][0] + " --> " + e.args[0]

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
        conn.execute("""CREATE TABLE dmoz (title TEXT, link TEXT, desc TEXT)""")
        conn.commit()
        return conn