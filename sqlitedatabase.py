import sqlite3
from datetime import datetime
import random

conn = sqlite3.connect(":memory:")

c = conn.cursor()
tablenames = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]

for names in tablenames:
    c.execute("""CREATE TABLE {} (
        DateTime text,
        Temperature integer,
        Humidity integer
        )""".format(names))

for names in tablenames:
    now = datetime.now()
    Temp = random.randrange(16,40)
    Humid = random.randrange(0,100)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    c.execute("INSERT INTO {} VALUES (?,?,?)".format(names),(dt_string,Temp,Humid))
    conn.commit()

for names in tablenames:
    c.execute("SELECT * FROM {}".format(names))
    print(c.fetchall())

conn.commit()
conn.close()