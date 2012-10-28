#!/usr/bin/python
'''
'''

import serial
import time
import random
import array
import os
import datetime

class Communicate:
    def __init__(self, serial_port):
        self._serial_port = serial_port
        self._open_serial()
        self._flush()

    def _open_serial(self):
        self._handle = serial.Serial(self._serial_port, 115200, timeout=0.1)

    def _reset(self):
        """
        doesn't work with pyserial.
        should be implemented with pyftdi
        """
        self._handle.setDTR(False)
        time.sleep(1)
        self._handle.setDTR(True)
        time.sleep(1)

    def _flush(self):
        self._handle.flush()
        self._handle.flushInput()
        self._handle.flushOutput()
        # time.sleep(1)

    def send(self, data, log=True):
        # data_string = array.array('B', data).tostring()
        # self._handle.write(data_string)
        self._handle.write(data)
        if log:
            self.saveLog()

    def read(self):
        # time.sleep(5)
        # print self.handle.read(1000)
        received = ''
        read_data= True
        while read_data:
            time.sleep(1)
            read_data = self._handle.read(1000)
            received +=read_data
        if received:
            print received,
        return received

    def saveLog(self):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = myCom.read()#read output from bus pirate
        with open("out.txt", "a") as myfile:
            myfile.write('\n'+date_str+'\n')#save date to file
            myfile.write(lines)#save data from bus pirate to file

if __name__ == '__main__':
    myCom = Communicate('/dev/ttyUSB0')
    myCom.send('m\n2\n')#bus pirate: select 1 wire mode (in default mode/hiz mode external power supply can not be set
    while True:
        Count = 10
        myCom.send('W\n')#bus pirate: power supplies on
        while Count:
            Count -= 1
            myCom.send('f\n')#bus pirate: measure frequency on the AUX pin
        myCom.send('w\n')#bus pirate: power supplies off
        time.sleep(5*60)
