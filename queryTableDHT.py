import sqlite3
conn=sqlite3.connect('sensorsData.db')
curs=conn.cursor()

maxTemp = 22.5

print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM DHT_data"):
    print (row)

print ("\nDatabase entries for a specific humidity value:\n")
for row in curs.execute("SELECT * FROM DHT_data WHERE hum='29'"):
    print (row)
    
print ("\nDatabase entries where the temperature is above 30oC:\n")
for row in curs.execute("SELECT * FROM DHT_data WHERE temp>30.0"):
    print (row)
    
print ("\nDatabase entries where the temperature is above x:\n")
for row in curs.execute("SELECT * FROM DHT_data WHERE temp>(?)", (maxTemp,)):
    print (row)
