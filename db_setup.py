import sqlite3


conn = sqlite3.connect('comtrade.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE INGREDIENTS 
       (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
       COMMODITY      INT     NOT NULL UNIQUE,
       REGION         INT     NOT NULL,
       DATA           TEXT    NOT NULL);''')
print("Table created successfully")

conn.close()
