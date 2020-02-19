from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time

def lorainit():
    global lora

    BOARD.setup()
    lora = LoRa()
    lora.set_mode(MODE.STDBY)
    lora.set_freq(915.0) #set to 915MHz for SG use

def main():
    lorainit()
    lora.set_mode(MODE.RXCONT) #Switch to recieve modes
    while True:
        if (payload = lora.read_payload(nocheck=True)):
            print(bytes(payload).decode("utf-8",'ignore'))
        time.sleep(0.1)

if __name__ == "__main__":
    main()