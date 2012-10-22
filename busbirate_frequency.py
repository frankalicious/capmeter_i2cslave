#!/usr/bin/python
'''
testing complete communication
(uart->rfm12) -> (rfm12->i2c)
(i2c->rfm12) -> (rfm12->uart)
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

    def send(self, data):
        # data_string = array.array('B', data).tostring()
        # self._handle.write(data_string)
        self._handle.write(data)

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

if __name__ == '__main__':
    myCom = Communicate('/dev/ttyUSB0')
# for address in [x<<1 for x in range(1,128)]:
# for address in [0x12,0x18]:
# for address in [0x12]:
    # data = [address, ord('a')]
    # data = [address, ord('g')]
    # data_string = array.array('B', data).tostring()
    # HANDLE.write(data_string)
    # time.sleep(1)
    # print HANDLE.read(1000)


# address_blinkm_mini = [0x12]
# address_blinkm_hp = [0x18]
# address = address_blinkm_hp
    # myCom.send(address=0x12, command=ord('a'))
    # myCom.send(address=0x12, command=ord('a'))
    while True:
        lines = myCom.read()
        with open("out.txt", "a") as myfile:
            myfile.write(lines)
            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            myfile.write('\n'+date_str+'\n')
        myCom.send('f\n')
        time.sleep(1)
# command = [ord('g')]
# command = [ord('g')]
# command = [ord('c'),255,255,0]
# command = [ord('Z')]
# command = [ord('R'),0,0]
# command = [ord('o')]
# command = [ord('p'), 10,0,0]
# command = [ord('t'), 100]
