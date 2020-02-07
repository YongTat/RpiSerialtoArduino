from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time

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
    lora.set_mode(MODE.RXCONT) #recieve mode

"""
Recieves data from lora in the format [asciidata, asciidata, asciidata, ... ,10] 10 is the ascii
for new line
"""
def reciever():
    lora.set_mode(MODE.RXCONT) #Switch to recieve mode
    payload = lora.read_payload(nocheck=True)
    #print ("Receive: ")
    #print(bytes(payload).decode("utf-8",'ignore')) # Receive DATA
    return(bytes(payload).decode("utf-8",'ignore'))

def main():
    lorainit()


if __name__ == "__main__":
    main()