# from SX127x.LoRa import *
# from SX127x.board_config import BOARD
import time

"""
A function to simulate picking list from server
"""
def inittester(scannerin):
    zerotoend = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    if scannerin == "1":
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
Converts a string into a ascii list for sending over lora
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

def sender(asciiin):
    lora.write_payload([asciiin])
    lora.set_mode(MODE.TX) 
    lora.set_mode(MODE.RXCONT)

def main():
    lorainit()
    scannerin = input("Scanner Input")
    pickinglist = inittester(scannerin)
    asciipickinglist = stringtoascii(pickinglist)
    print(asciipickinglist)
    for item in asciipickinglist:
        sender(item)
        time.sleep(1)


if __name__ == "__main__":
    main()