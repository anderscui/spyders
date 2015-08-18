import sqlite3 as sqlite

car_id = 1

con = sqlite.connect('test.db')

with con:

    cur = con.cursor()
    cur.execute('SELECT Name, Price FROM Cars WHERE Id = :Id', {"Id": car_id})
    con.commit()

    row = cur.fetchone()
    print row[0], row[1]