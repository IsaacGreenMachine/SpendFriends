import sqlite3
from tokenize import String
import uuid
import json
import datetime

con = sqlite3.connect('../example.db')#, check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute("UPDATE lists set incomes ='[]' WHERE list_id='d2ebfe2d-c04f-4b9f-976a-480c271575ac'")

con.commit()
con.close()
