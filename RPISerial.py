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
    writetoserial("3")
    readfromserial()

if __name__ == "__main__":
    main()
