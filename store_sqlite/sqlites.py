import sqlite3

# print(sqlite3.version)
# print(sqlite3.sqlite_version)

import sys

con = None
try:
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    cur.execute('select SQLITE_VERSION()')

    data = cur.fetchone()
    print('SQLite version: %s' % data)

except sqlite3.Error, e:
    print('Error: %s' % e.args[0])
    sys.exit(1)

finally:
    if con:
        con.close()

