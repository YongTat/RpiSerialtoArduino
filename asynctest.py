from SX127x.LoRa import *
from SX127x.board_config import BOARD
import multiprocessing
import time
import requests
import sqlite3
import re
from datetime import datetime

def lorainit():
    global lora

    BOARD.setup()
    lora = LoRa(verbose=False)
    lora.set_mode(MODE.STDBY)
    lora.set_freq(923.0) #set to 915MHz for SG use


def stringtoascii(stringlist):
    """
    Takes in a list in the format [data, data, data, ...] and converts
    to [[asciidata], [asciidata], [asciidata]].
    """
    finalstring = []
    asciistring = []
    for item in stringlist:
        for s in str(item):
            asciistring.append(ord(str(s)))
        finalstring.append(asciistring)
        asciistring = []
    return finalstring

def asciitostring(asciilist):
    """
    Takes in a list in the format [asciidata, asciidata, asciidata, ... ,10] and converts it back to string(needs testing)
    """
    removenl = asciilist.pop #removes the 10 from the tail
    finalstr = ""
    for item in removenl:
        finalstr += str(chr(item))
    return finalstr


def sender(asciiin):
    """
    Takes in data in the format of [asciidata] and sends it thru lora. The longer the message the longer delya you need
    """
    lora.write_payload(asciiin)
    lora.set_mode(MODE.TX) #send mode
    time.sleep(0.04)
    lora.set_mode(MODE.RXCONT) #recieve mode


def listenmode():
    """
    Listening mode for when you are not sending packets.
    """
    lora.set_mode(MODE.RXCONT) #Switch to recieve modes
    conn = sqlite3.connect("sensor.db")
    c = conn.cursor()
    pattern = re.compile(r"^([A][CNS0-9]+)+\%$")
    while True:
        payload = lora.read_payload(nocheck=True)
        if (payload != []):
            text = str(bytes(payload).decode("utf-8",'ignore'))
            print(text)
            name = text[0:text.find("N")]
            if (pattern.match(text)):
                if (text.find("S") > 0):
                    pos = text.find("S")
                    #Write data to local DB
                    temp = int(text[pos+1:pos+3])
                    humid = int(text[pos+4:pos+6])
                    now = datetime.now()
                    dt_string = dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    with conn:
                        c.execute("INSERT INTO {} VALUES (?,?,?)".format(name),(dt_string,temp,humid))
            # something like packet flushing after receive
            payload = []
            lora.set_mode(MODE.SLEEP)
            lora.reset_ptr_rx()
            lora.set_mode(MODE.RXCONT)
        time.sleep(0.05) #longer packet needs longer delay

def main():
    lorainit()
    while True:
        p1 = multiprocessing.Process(target=listenmode)
        p1.start()
        userin = input("Enter: ")
        p1.terminate()
        asciiinput = stringtoascii([userin])
        for item in asciiinput:
            sender(item)

if __name__ == "__main__":
    main()