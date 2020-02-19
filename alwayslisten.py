from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time
import requests

def lorainit():
    global lora

    BOARD.setup()
    lora = LoRa(verbose=False)
    lora.set_mode(MODE.STDBY)
    lora.set_freq(915.0) #set to 915MHz for SG use

def main():
    lorainit()
    lora.set_mode(MODE.RXCONT) #Switch to recieve modes
    while True:
        payload = lora.read_payload(nocheck=True)
        if (payload != []):
            text = str(bytes(payload).decode("utf-8",'ignore'))
            payload = {
                "Name": text[0:2],
                "Temp": text[2:4],
                "Humidity": text[4:6]
            }
            r = requests.post("http://192.168.137.142:1880/Sensorin", data=payload)
            payload = []
            lora.set_mode(MODE.SLEEP)
            lora.reset_ptr_rx()
            lora.set_mode(MODE.RXCONT)
        time.sleep(0.1)

if __name__ == "__main__":
    main()