import sqlite3
from tokenize import String
import uuid
import json
import datetime

con = sqlite3.connect('../example.db')#, check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

#print(cur.execute("SELECT username FROM users WHERE user_id = '{}'".format("579cd04e-0516-4443-9f69-739cfe397db7")).fetchall()[0][0])
cur.execute("UPDATE users SET lists = '{}' where username = '{}'".format(json.dumps(['1000', '201230', '450340']), "newUser1012"))

ls = cur.execute("SELECT lists FROM users WHERE username = '{}'".format("newUser1012")).fetchall()[0][0]
ls = json.loads(ls)
ls.append('101245313532')
cur.execute("UPDATE users SET lists = '{}' where username = '{}'".format(json.dumps(ls), "newUser1012"))
con.commit()
con.close()
