import sqlite3 as sqlite

con = sqlite.connect('lagou.db')

with con:

    con.row_factory = sqlite.Row
    cur = con.cursor()
    # cur.execute('SELECT pos_id, desc, created_on FROM position where pos_id = 90379')
    # cur.execute('SELECT pos_id, desc, created_on FROM position where pos_id = 900032')
    cur.execute('SELECT pos_id, desc, created_on FROM position where pos_id = 42')
    row = cur.fetchone()

    # print(type(rows))

    if row:
        print 'found'
        print row['pos_id'], row['desc'], row['created_on']
    else:
        print 'not found'

    row_exists, desc_exists = False, False
    if row:
        row_exists = True
        if row['desc'] != 'n/a':
            desc_exists = True

    print row_exists, desc_exists