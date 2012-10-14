#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

with open('out.txt', 'r') as f:
     read_data = f.read()

low=[]
high=[]
for line in read_data.splitlines():
     if not ('[L]' in line or '[H]' in line):
          continue

     splitted = line.split()
     # ['[L]', '1.365', 'uF']
     print splitted
     try:
          value = float(splitted[1])
     except (ValueError,IndexError):
          continue
          
     if splitted[2] == 'mF':
          decades = 10**-3

     elif splitted[2] == 'uF':
          decades = 10**-6

     elif splitted[2] == 'nF':
          decades = 10**-9

     elif splitted[2] == 'pF':
          decades = 10**-12

     else :
          decades = 1

     # print value * decades

     if splitted[0] == '[H]':
          high.append(value * decades)
     if splitted[0] == '[L]':
          low.append(value * decades)
# print high
plt.plot(high)
plt.plot(low)
plt.show()
