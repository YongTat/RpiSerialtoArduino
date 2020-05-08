import sqlite3
from datetime import datetime
import random
import time

tablenames = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]

def maketables(tablenames):
    for names in tablenames:
        try:
            c.execute("""CREATE TABLE {} (
                DateTime text,
                Temperature integer,
                Humidity integer
                )""".format(names))
        except:
            pass

def adddata(numberofdata):
    for _ in range(numberofdata):
        for names in tablenames:
            now = datetime.now()
            Temp = random.randrange(16,40)
            Humid = random.randrange(0,100)
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            c.execute("INSERT INTO {} VALUES (?,?,?)".format(names),(dt_string,Temp,Humid))
    conn.commit()

def showdata():
    for names in tablenames:
        c.execute("SELECT * FROM {}".format(names))
        print(c.fetchall())

def getlastdata(tablename):
    data = c.execute("SELECT * FROM {}".format(tablename))
    final = list(data)
    return final[-1]

if __name__ == "__main__":
    conn = sqlite3.connect("sensor.db")
    c = conn.cursor()
    maketables(tablenames)
    # adddata(10)
    # showdata()
    # ans = getlastdata("A10")
    # print(ans)
    conn.commit()
    conn.close()