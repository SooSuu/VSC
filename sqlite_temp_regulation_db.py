import sqlite3

conn = sqlite3.connect('sensorsData.db')
print ('Opened database successfully')

conn.execute('CREATE TABLE TEMP_R (ID INTEGER, CREATED_AT DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, MAX INT NOT NULL, MIN INT NOT NULL, PRIMARY KEY(ID))')
print ('Table created successfully')
conn.close()