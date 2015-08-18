import sqlite3 as sqlite

con = sqlite.connect('test.db')

with con:

    cur = con.cursor()
    cur.execute('SELECT * FROM Cars')

    while True:
        row = cur.fetchone()
        if not row:
            break

        print row[0], row[1], row[2]

    