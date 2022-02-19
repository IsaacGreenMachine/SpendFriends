from cmath import exp
import sqlite3
from tokenize import String
import uuid
import json
import datetime

from simplejson import dumps
con = sqlite3.connect('../example.db')#, check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

con.execute('DROP TABLE IF EXISTS users')
con.execute('DROP TABLE IF EXISTS lists')

# Create table
cur.execute('''CREATE TABLE users(
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    user_id TEXT PRIMARY KEY,
    lists TEXT,
    friends TEXT,
    settings TEXT
    )''')
# user_id : uuid.4
# lists: ["list_id", "list_id", ...]
# friends: ["user_id", "user_id", ...]
# settings: []


cur.execute('''CREATE TABLE lists(
    list_name TEXT NOT NULL,
    list_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    owner_name TEXT,
    categories TEXT,
    expenses TEXT,
    incomes TEXT,
    shared_users TEXT,
    settings TEXT
    )''')
# list_id: uuid.4
# owner_id: user_id
# categories: []
# expenses: [['exp_id', 'exp_amt', 'exp_name', 'exp_desc'], ['exp_id', 'exp_amt', 'exp_name', 'exp_desc'], ...]
# incomes: [['exp_id', 'exp_amt', 'exp_name', 'exp_desc'], ['exp_id', 'exp_amt', 'exp_name', 'exp_desc'], ...]
# shared_users: ['usr_id', 'usr_id', 'usr_id' ...]
# settings: []

isaacUserid = uuid.uuid4()
# Create user isaacUser
cur.execute("INSERT INTO users VALUES ('{}','{}', '{}', '{}', '{}', '{}')".format(
    "isaacUser",
    "ivg123",
    str(isaacUserid),
    json.dumps([]), # lists
    json.dumps([]), # friends
    json.dumps([]) # settings
    )
)

# Create user user1
cur.execute("INSERT INTO users VALUES ('{}','{}', '{}', '{}', '{}', '{}')".format(
    "user1",
    "test1",
    str(uuid.uuid4()),
    json.dumps([]),
    json.dumps([]),
    json.dumps([])
    )
)

# Create list isaacList1
isaacList1_id = str(uuid.uuid4())
cur.execute("INSERT INTO lists VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
    "isaacList",
    isaacList1_id,
    str(isaacUserid),
    "isaacUser",
    json.dumps([]), #categories
    json.dumps([['haircut' , 90.56, 'self care'], ['video Game' , 20, 'entertainment']]), #expenses
    json.dumps([['work' , 100, 'full time'], ['side job' , 5, 'part time']]), #incomes
    json.dumps([]), #shared_users
    json.dumps([]) #settings
    )
)

# Save (commit) changes
con.commit()
response = cur.execute('SELECT * FROM users where username = "{}"'.format("isaacUser")).fetchall()
#print(dir(response))
for r in response:
    dic = {r.keys()[i]: r[i] for i in range(len(r))}
    #print(dic)
    #if "isaacUser" in i:
        #print("YUP!")
for r in cur.execute('SELECT * FROM lists').fetchall()[0]:
    print(r)

print(cur.execute("SELECT user_id FROM users where username = '{}'".format('isaacUser')).fetchall()[0][0])

print(cur.execute('SELECT * FROM users where username = "{}"'.format("isaacUserhaha")).fetchall())
#lists all tables
#print(con.execute('SELECT name FROM sqlite_master').fetchall())

#print(con.execute('SELECT * FROM users').fetchall())
#print(json.loads(cur.execute('SELECT friends FROM users WHERE username = "{}"'.format("isaacUser")).fetchall()[0][0]))
#print(cur.execute('SELECT user_id FROM users WHERE username = "{}"'.format("isaacUser")).fetchall()[0][0])

#drop table
#con.execute('DROP TABLE stocks')

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
