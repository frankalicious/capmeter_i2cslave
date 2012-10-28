#!/usr/bin/python
import numpy
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date
import scipy
import pprint
from datetime import datetime, timedelta

#filtering http://www.swharden.com/blog/2009-01-21-signal-filtering-with-python/
#http://www.scipy.org/Cookbook/SignalSmooth
# DEBUG = True
DEBUG = False

def mean(numberList):
    if len(numberList) == 0:
        return float('nan')
 
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

# http://glowingpython.blogspot.de/2011/08/how-to-plot-frequency-spectrum-with.html
def plotSpectrum(y,Fs):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = scipy.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    Y = scipy.fft(y)/n # fft computing and normalization
    # for i in range(len(Y)): # frankalicious added filtering
        # if i<=1000:
            # Y[i]=0

    Y = Y[range(n/2)]
 
    plt.plot(frq,abs(Y),'r') # plotting the spectrum
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')

def smoothListGaussian(list,strippedXs=False,degree=5):  

    window=degree*2-1  
    weight=numpy.array([1.0]*window)  
    weightGauss=[]  

    for i in range(window):  
        i=i-degree+1  
        frac=i/float(window)  
        gauss=1/(numpy.exp((4*(frac))**2))  
        weightGauss.append(gauss)  

    weight=numpy.array(weightGauss)*weight  
    smoothed=[0.0]*(len(list)-window)  

    for i in range(len(smoothed)):  
        smoothed[i]=sum(numpy.array(list[i:i+window])*weight)/sum(weight)  

    return smoothed

def get_data():
    with open('out.txt', 'r') as f:
        raw_data = f.read()
    return raw_data

def parse_data(read_data):
    parsed = {}
    parsed['freq'] = []
    parsed['date'] = []
    # parsed['low_errors'] = 0
    # parsed['high_errors'] = 0

    #we expect first date then the frequency
    expect_date = True
    for line in read_data.splitlines():
        splitted = line.split()
        if any("2012" in s for s in splitted) and expect_date:
            mydate = ' '.join(splitted)
            mydate_num = date2num(datetime.strptime(mydate,"%Y-%m-%d %H:%M:%S"))
            parsed['date'].append(mydate_num)
            expect_date = False
            # print mydate_num

            # datetime.strptime('2012-10-22 19:53:12',"%Y-%m-%d %H:%M:%S")
            
        if 'Hz' in splitted and not expect_date:
            raw_value = splitted[-2]
            # print parsed['freq']
            if ',' in raw_value:#we don't use these strange values
                print num2date(parsed['date'][-1]), splitted
                # print splitted
                # print raw_value,
                # raw_value = raw_value.replace(',','')
                # print raw_value,
                # print parsed['date'][-1]
                parsed['date'].pop()#check if we have to remove tha last one or the next one

            else:
                parsed['freq'].append(raw_value)
                expect_date = True
            # parsed['freq'].append(raw_value)
 
    if DEBUG:
        print "len(parsed['date']):", len(parsed['date'])
        print "len(parsed['freq']):", len(parsed['freq'])

    #fix length
    if len(parsed['date']) > len(parsed['freq']):
        print 'cutting down date list'
        parsed['date'] = parsed['date'][0:len(parsed['freq'])]
    elif len(parsed['freq']) > len(parsed['date']):
        print 'cutting down frequency list'
        parsed['freq'] = parsed['freq'][0:len(parsed['date'])]
        
    return parsed



raw_data = get_data()
parsed_data = parse_data(raw_data)

# print 'count of high errors:', parsed_data['high_errors']
# print 'count of low errors:', parsed_data['low_errors']

#only use last 4000 examples
parsed_data['date'] = parsed_data['date'][-4000:]
parsed_data['freq'] = parsed_data['freq'][-4000:]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
# pprint.pprint (parsed_data)
ax.plot_date(parsed_data['date'],parsed_data['freq'],'b-',xdate=True)
ax.plot_date(parsed_data['date'],parsed_data['freq'],'ro',xdate=True)

# Set the xtick locations to correspond to just the dates you entered.
# ax.set_xticks(parsed_data['date'])

# Set the xtick labels to correspond to just the dates you entered.
# graph.set_xticklabels(
        # [date.strftime("%Y-%m-%d") for (date, value) in data]
        # )

plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# # # ax = fig.add_subplot(3,1,1)
# # ax.set_color_cycle(['r'])
# ax.plot(parsed_data['high'])
# ax.set_yscale('log')
# ax.set_title('high logarithmic')

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# # ax = fig.add_subplot(3,1,2)
# # ax.set_color_cycle(['b'])
# ax.plot(parsed_data['low'])
# # ax.plot(parsed_data['low'][:-2000:])
# ax.set_yscale('log')
# ax.set_title('low logarithmic')

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# # ax = fig.add_subplot(3,1,3)
# ax.set_color_cycle(['r', 'b'])
# ax.plot(parsed_data['high'])
# ax.plot(parsed_data['low'])
# ax.set_title('high and low')

# fig = plt.figure()
# # ax = fig.add_subplot(2,1,1)
# ax = fig.add_subplot(1,1,1)
# fft=scipy.fft(parsed_data['low'])
# ax.set_title('fft of low signal')
# # bp=fft[:]
# N = len(parsed_data['low'])
# sample_rate = 1000.0#don't know samplerate
# f=sample_rate*parsed_data['low'][0:(N/2)]/N

# # ax.plot(abs(bp[2000:-2000:]))
# ax.set_yscale('log')
# # ax.plot(abs(bp))
# n=len(f)
# ax.plot(f,abs(fft[0:n])/N)
# # for i in range(len(bp)): # (H-red)  

# #     if i>=10:bp[i]=0  
# # ax = fig.add_subplot(2,1,2)
# # fft=scipy.fft(parsed_data['low'])
# # ax.set_title('ifft/fft filtered low signal')
# # ibp=scipy.ifft(bp)

# # ax.plot(ibp/max(ibp))
# plotSpectrum(parsed_data['low'],1000.0)

# window_len = len(parsed_data['low'])
# w=numpy.ones(window_len,'d')
# y=numpy.convolve(w/w.sum(),parsed_data['low'],mode='valid')
# print y
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.plot(y)

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# # ax.plot(smoothListGaussian(parsed_data['high']))
# ax.plot(smoothListGaussian(parsed_data['high'], False, 100))
# ax.set_title('gaussian filtered high signal')

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# # ax.plot(smoothListGaussian(parsed_data['low']))
# ax.plot(smoothListGaussian(parsed_data['low'], False, 100))
# ax.set_title('gaussian filtered low signal')

# ax.plot(smoothListGaussian(parsed_data['low']))
# ax.plot(smoothListGaussian(parsed_data['low'], False, 100))
# ax.set_title('gaussian filtered low signal')

# plt.show()
