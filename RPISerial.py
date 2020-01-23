import serial
import time

ser = serial.Serial('COM10', 9600, timeout=2)
print(ser.name)

line = ser.readlines()
print(line)

string1 = "3\n"

ser.write(string1.encode())

line = ser.readlines()
print(line)

quit()