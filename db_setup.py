import sqlite3


conn = sqlite3.connect('comtrade.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE INGREDIENTS 
       (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
       COMMODITY      INT     NOT NULL UNIQUE,
       REGION         INT     NOT NULL,
       COUNTRY_CODE   CHAR(4)    NOT NULL);''')
print("Table created successfully")

conn.close()
