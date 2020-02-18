from SX127x.LoRa import *
from SX127x.board_config import BOARD

"""
Always listens and prints out packets
"""
def alwayslisten():
    lora.set_mode(MODE.RXCONT) #Switch to recieve mode
    payload = lora.read_payload(nocheck=True)
    print(bytes(payload).decode("utf-8",'ignore'))

def main():
    while True:
        alwayslisten()

if __name__ == "__main__":
    main()