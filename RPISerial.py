import serial
import time

def initserial():
    global ser
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

def readfromserial():
    line = ser.readlines()
    print(line)

def writetoserial(stringwrite):
    newstringwrite = stringwrite + "\n"
    ser.write(newstringwrite.encode())

def main():
    initserial()
    readfromserial()
    scannerin = input("Scan: ")
    writetoserial(str(scannerin))
    readfromserial()

if __name__ == "__main__":
    main()

"""
Code to Test
    For windows only
    ser.serial.Serial()
    ser.baudrate = 9600
    ports = serial.tools.list_ports.comports(include_links=False)
    for port in ports :
        print(port.device)
        ser.port = port.device
        try:
            ser.is_open()
        except:
            continue

"""