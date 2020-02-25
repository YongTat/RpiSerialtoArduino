from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time
import requests

thingsspeakapikeys = {
    "A5": "5J9C9RM334D695X3",
    "A4": "1J14O7KG9I2JB7GY"
}

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
            name = text[0:text.find("N")]

            if (text.find("S") > 0):
                pos = text.find("S")
                # payload = {
                #     "Name": name,
                #     "Temp": text[pos+1:pos+4],
                #     "Humidity": text[pos+4:pos+7]
                # }
                # r = requests.post("http://192.168.137.142:1880/Sensorin", data=payload)
                payload = {
                    "api_key": thingsspeakapikeys.get(name),
                    "field1": text[pos+1:pos+3],
                    "field2": text[pos+4:pos+6],
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

if __name__ == "__main__":
    main()

#<Device Name>NL<LED State>
#<Device Name>NS<Temp"C"><Humidity"%"">