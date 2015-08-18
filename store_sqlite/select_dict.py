import sqlite3 as sqlite

con = sqlite.connect('test.db')

with con:

    con.row_factory = sqlite.Row

    cur = con.cursor()
    cur.execute('SELECT * FROM Cars')

    rows = cur.fetchall()
    for row in rows:
        print('%s %s %s' % (row['id'], row['name'], row['PRICE']))