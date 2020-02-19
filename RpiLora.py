from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time
import sys
import requests

"""
A function to simulate picking list from server, might change if using django frontend?
"""
def inittester(scannerin):
    zerotoend = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    if scannerin == 1:
        return zerotoend
    else:
        return zerotoend.reverse()

def lorainit():
    global lora

    BOARD.setup()
    lora = LoRa()
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
Takes in data in the format of [asciidata] and sends it thru lora
"""
def sender(asciiin):
    lora.write_payload(asciiin)
    lora.set_mode(MODE.TX) #send mode
    lora.reset_ptr_rx()
    lora.set_mode(MODE.RXCONT) #recieve mode

"""
Recieves data from lora in the format [asciidata, asciidata, asciidata, ... ,10] 10 is the ascii
for new line
"""
def reciever():
    lora.set_mode(MODE.RXCONT) #Switch to recieve mode
    payload = lora.read_payload(nocheck=True)
    text = bytes(payload).decode("utf-8",'ignore')
    lora.set_mode(MODE.SLEEP)
    lora.reset_ptr_rx()
    lora.set_mode(MODE.RXCONT)
    return(str(text))

def main():
    lorainit()
    # grabs input from scanner and prepares to send instructions over lora
    #Node Red Input
    scannerin = sys.argv[1]
    #scannerin = input("Scannerinput")
    asciiinput = stringtoascii([scannerin])
    for item in asciiinput:
        cfmflag = False
        sendcount = 0
        while (cfmflag == False):
            sender(item)
            if (sendcount > 1):
                #add fail detection here
                break
            timeout = int(time.time()) + 1
            # waits for confirm recieve
            while (int(time.time()) != timeout):
                dataget = reciever()
                if dataget[0:2] == scannerin[0:2]:
                    #add post request here
                    payload = {
                        "Name": scannerin[0:2],
                        "Data": dataget[2:3]
                    }
                    r = requests.post("http://192.168.137.142:1880/LEDin", data=payload)
                    cfmflag = True
                    break
                else:
                    time.sleep(0.1)
            if (not cfmflag):
                sender(item)
                sendcount += 1
                


if __name__ == "__main__":
    main()

"""

Pseudo Code

Input command

<DeviceName>LED

Device LED lights up and sends LED True Signal

<DeviceName>Temp

Gets Temp

<DeviceName>Humid

Gets Humidity

|| run in parallel(?)

Needs device lists

Every min ask device for analouge readings

"""