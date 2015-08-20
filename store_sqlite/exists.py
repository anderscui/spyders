import sqlite3 as sqlite

con = sqlite.connect('test.db')

with con:

    cur = con.cursor()

    car_id = 11
    car_price = 21000
    cur.execute('SELECT EXISTS(SELECT 1 FROM Cars WHERE Id = ?)', (car_id,))

    if cur.fetchone()[0]:
        print('Found')
    else:
        print('Not Found')