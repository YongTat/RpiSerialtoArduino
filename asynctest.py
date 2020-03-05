from SX127x.LoRa import *
from SX127x.board_config import BOARD
import multiprocessing
import time
import requests

thingsspeakapikeys = {
    "A5": "5J9C9RM334D695X3",
    "A4": "1J14O7KG9I2JB7GY",
    "0" : "K0GBV7LQY0FWSWNB",
    "1" : "5WYCGS9GF263QFO4"
}

fieldnumber = {
    "1" : ["field1", "field2"],
    "2" : ["field3", "field4"],
    "3" : ["field5", "field6"],
    "4" : ["field7", "field8"]

}

def lorainit():
    global lora

    BOARD.setup()
    lora = LoRa(verbose=False)
    lora.set_mode(MODE.STDBY)
    lora.set_freq(915.0) #set to 915MHz for SG use

"""
Takes in a list in the format [data, data, data, ...] and converts
to [[asciidata], [asciidata], [asciidata]].
"""
def stringtoascii(stringlist):
    finalstring = []
    asciistring = []
    for item in stringlist:
        for s in str(item):
            asciistring.append(ord(str(s)))
        finalstring.append(asciistring)
        asciistring = []
    return finalstring

"""
Takes in a list in the format [asciidata, asciidata, asciidata, ... ,10] and converts it back to string(needs testing)
"""
def asciitostring(asciilist):
    removenl = asciilist.pop #removes the 10 from the tail
    finalstr = ""
    for item in removenl:
        finalstr += str(chr(item))
    return finalstr

"""
Takes in data in the format of [asciidata] and sends it thru lora. The longer the message the longer delya you need
"""
def sender(asciiin):
    lora.write_payload(asciiin)
    lora.set_mode(MODE.TX) #send mode
    time.sleep(0.04)
    lora.set_mode(MODE.RXCONT) #recieve mode

"""
Listening mode for when you are not sending packets.
"""
def listenmode():
    lora.set_mode(MODE.RXCONT) #Switch to recieve modes
    while True:
        payload = lora.read_payload(nocheck=True)
        if (payload != []):
            text = str(bytes(payload).decode("utf-8",'ignore'))
            name = text[0:text.find("N")]

            if (text.find("S") > 0):
                pos = text.find("S")
                id = (int(text[1:pos])-1) / 4
                print(id)
                field = (int(text[1:pos])-1) % 4
                # payload = {
                #     "Name": name,
                #     "Temp": text[pos+1:pos+4],
                #     "Humidity": text[pos+4:pos+7]
                # }
                # r = requests.post("http://192.168.137.142:1880/Sensorin", data=payload)
                payload = {
                    "api_key": thingsspeakapikeys.get(id),
                    field[0]: text[pos+1:pos+3],
                    field[1]: text[pos+4:pos+6],
                }
                r = requests.post("https://api.thingspeak.com/update.json", data=payload)

            elif (text.find("L") > 0):
                pos = text.find("L")
                payload = {
                            "Name": name,
                            "Data": text[pos+1:pos+2]
                        }
                r = requests.post("http://localhost:1880/LEDin", data=payload)
            
            payload = []
            lora.set_mode(MODE.SLEEP)
            lora.reset_ptr_rx()
            lora.set_mode(MODE.RXCONT)
        time.sleep(0.1)

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