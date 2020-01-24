import serial
import serial.tools.list_ports as lp
import time

def initserial():
    global ser
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.timeout = 2
    ports = lp.comports(include_links=False)
    for port in ports:
        print(port.device)
        print(port.manufacturer)
	manufacturer = port.manufacturer
	if "arduino" in manufacturer.lower():
		ser.port = port.device
		break
    ser.open()

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
