import serial
import serial.tools.list_ports as lp
import time

def initserial():
    global ser
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.timeout = 2
    ports = lp.comports(include_links=False)
    #Finding the port the arduino is connected to
    for port in ports:
        #print(port.device)
        #print(port.manufacturer)
        manufacturer = port.manufacturer
        if "arduino" in manufacturer.lower():
            ser.port = port.device
            break
    ser.open()

def readfromserial():
    line = ser.readlines()
    return line

def writetoserial(stringwrite):
    newstringwrite = stringwrite + "\n"
    ser.write(newstringwrite.encode())

"""
To do next, use list.sort to sort the list
"""

def main():
    initserial()
    print(readfromserial())
    scannerin = input("Scan: ")
    writetoserial(str(scannerin))
    print(readfromserial())

if __name__ == "__main__":
    main()
