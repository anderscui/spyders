import sqlite3 as sqlite

con = sqlite.connect('test.db')

with con:

    cur = con.cursor()
    cur.execute('PRAGMA table_info(Cars)')

    data = cur.fetchall()
    print 'Columns: '
    print 'order \t name \t type \t nullable \t default'
    for d in data:
        print d[0], d[1], d[2], d[3], d[4]

    print 'All tables: '
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    rows = cur.fetchall()
    for row in rows:
        print row[0]

