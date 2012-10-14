#!/usr/bin/python
# http://www.bemasher.net/archives/813
import serial, os

ser = serial.Serial('/dev/ttyACM3', 19200)
while True:
    line = ser.readline().strip()
    os.system("echo %s>>out.txt" % (line))
    print line

