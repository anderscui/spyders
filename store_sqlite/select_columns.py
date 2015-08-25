import sqlite3 as sqlite

con = sqlite.connect('test.db')

with con:

    con.row_factory = sqlite.Row
    cur = con.cursor()
    cur.execute('SELECT name FROM Cars')
    rows = cur.fetchall()

    print(type(rows))

    names = [row['name'] for row in rows]

    print(names)