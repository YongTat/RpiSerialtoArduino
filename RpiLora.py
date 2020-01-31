from SX127x.LoRa import *
from SX127x.board_config import BOARD

def lorainit():
    global lora

    BOARD.setup()
    lora = LoRa()
    lora.set_mode(MODE.STDBY)
    lora.set_freq(915.0) #set to 915MHz for SG use

"""
Converts a string into a ascii list for sending over lora
"""
def stringtoascii(string):
    asciistring = []
    for s in string:
        asciistring.append(ord(s))
    return asciistring

def sender(asciilist):
    lora.write_payload([asciilist])
    lora.set_mode(MODE.TX) 
    lora.set_mode(MODE.RXCONT)

def main():
    pass

if __name__ == "__main__":
    main()