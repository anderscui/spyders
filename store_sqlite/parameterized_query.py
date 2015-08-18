import sqlite3 as sqlite

car_id = 1
car_price = 62300

con = sqlite.connect('test.db')

with con:

    cur = con.cursor()
    cur.execute('UPDATE Cars SET Price = ? WHERE Id = ?', (car_price, car_id))
    con.commit()

    print('Number of rows affected: %d' % cur.rowcount)