import sqlite3
from tokenize import String
import uuid
import json
import datetime

con = sqlite3.connect('../example.db')#, check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

#print(cur.execute("SELECT username FROM users WHERE user_id = '{}'".format("579cd04e-0516-4443-9f69-739cfe397db7")).fetchall()[0][0])
print(cur.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format("asbh", "dsljgkjb")).fetchall())
con.close()
