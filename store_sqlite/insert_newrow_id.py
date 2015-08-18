import sqlite3 as lite
import sys

con = lite.connect(':memory:')

with con:

    cur = con.cursor()

    cur.execute("CREATE TABLE Friends(Id INTEGER PRIMARY KEY, Name TEXT);")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Tom');")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Rebecca');")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Jim');")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Robert');")

    last_id = cur.lastrowid
    print 'The last id of the inserted row is %d' % last_id

