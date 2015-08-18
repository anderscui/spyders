import sqlite3

# print(sqlite3.version)
# print(sqlite3.sqlite_version)

import sys

con = sqlite3.connect('test.db')

with con:

    cur = con.cursor()
    cur.execute('select SQLITE_VERSION()')

    data = cur.fetchone()
    print('SQLite version: %s' % data)

