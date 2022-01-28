import sqlite3
from tokenize import String
import uuid
import json
import datetime
con = sqlite3.connect('../example.db')#, check_same_thread=False)
cur = con.cursor()

con.execute('DROP TABLE IF EXISTS users')
con.execute('DROP TABLE IF EXISTS expenses')
con.execute('DROP TABLE IF EXISTS incomes')

# Create table
#username text
#password text
#userid text
#settings? text
#link to expenses, income,
cur.execute('''CREATE TABLE users(
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    user_id TEXT PRIMARY KEY,
    categories TEXT,
    expenses TEXT,
    incomes TEXT,
    settings TEXT
    )''')

"""cur.execute('''CREATE TABLE expenses(
    text TEXT NOT NULL,
    category TEXT NOT NULL,
    amount TEXT PRIMARY KEY,
    settings TEXT,
    date TEXT NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
    )'''
)"""

# Insert a row of data
#cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
userid = uuid.uuid4()
cur.execute("INSERT INTO users VALUES ('isaacUser','ivg123', '{}', '', '', '', '')".format(userid))
#cur.execute("INSERT INTO expenses VALUES ('haircut','self care', '$44.91', '', '{}', '{}')".format(datetime.datetime.now(), userid))

cur.execute("UPDATE users SET expenses = '{}' WHERE user_id = '{}'".format(json.dumps([['haircut' , 90.56, 'self care'], ['video Game' , 20, 'entertainment']]), str(userid)))
cur.execute("UPDATE users SET incomes = '{}' WHERE user_id = '{}'".format(json.dumps([['work' , 100, 'full time'], ['side job' , 5, 'part time']]), str(userid)))
# Save (commit) changes
con.commit()

#prints a list of tuples from the database
#print(con.execute('SELECT * FROM stocks ORDER BY price').fetchall())

#lists all tables
print(con.execute('SELECT name FROM sqlite_master').fetchall())
print(con.execute('SELECT * FROM users').fetchall())
#print(con.execute('SELECT * FROM expenses').fetchall())
#drop table
#con.execute('DROP TABLE stocks')

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
