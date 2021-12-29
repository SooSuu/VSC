import sqlite3

conn = sqlite3.connect('sensorsData.db')
conn.execute('DROP TABLE VACCINE;')
print ('Opened database successfully')

conn.execute('CREATE TABLE VACCINE (ID INTEGER, CREATED_AT DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, NAME TEXT NOT NULL, EXPIRATION_DATE TEXT NOT NULL, PRIMARY KEY(ID))')
print ('Table created successfully')
conn.close()