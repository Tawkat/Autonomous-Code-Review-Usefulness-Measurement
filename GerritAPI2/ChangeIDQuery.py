import sys

reload(sys)
sys.setdefaultencoding('utf8')

import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import operator

connection=sqlite3.connect('Gerrit.db')
connection.text_factory=str
cursor=connection.cursor()

file=open("ChangeId.txt").read()
print(file)

cursor.execute("SELECT change_id FROM ReviewTable where reviewData=?",([file]))
data=cursor.fetchall()
print(data)
