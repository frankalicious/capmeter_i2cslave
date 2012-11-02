#!/usr/bin/python
import numpy
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date
import scipy
import pprint
from datetime import datetime, timedelta
from scipy import signal
import numpy

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

#http://azitech.wordpress.com/2011/03/15/designing-a-butterworth-low-pass-filter-with-scipy/
def plotSpectrum2(y, samp_rate):
    nsamps = len(y)
    # input signal spectrum
    xfreq = numpy.fft.fft(y)
    fft_freqs = numpy.fft.fftfreq(nsamps, d=1./samp_rate)
    fig = plt.figure()
    fig.add_subplot(111)
    ax = fig.add_subplot(1,1,1)

    plt.loglog(fft_freqs[0:nsamps/2], numpy.abs(xfreq)[0:nsamps/2])
    plt.title('Filter Input - Frequency Domain')
    # plt.text(0.03, 0.01, "freqs: "+str(freqs)+" Hz")
    plt.grid(True)

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
    parsed = []

    #we expect first date then the frequency
    for line in read_data.splitlines():
        splitted = line.split()
        if any("2012" in s for s in splitted):
            mydate = ' '.join(splitted)
            mydate_num = date2num(datetime.strptime(mydate,"%Y-%m-%d %H:%M:%S"))
            # datetime.strptime('2012-10-22 19:53:12',"%Y-%m-%d %H:%M:%S")
            
        if 'Hz' in splitted:
            raw_value = splitted[-2]
            raw_value = raw_value.replace(',','')#thousands are seperated with commas. remove them
            try:
                int_val = int(raw_value)
            except ValueError:
                print 'can\'t parse:', line
            
            else:
                parsed.append({'date': mydate_num, 'freq': int_val})
 
    if DEBUG:
        print "len(parsed):", len(parsed)
        
    return parsed

def plot_raw(date_list, frequency_list):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(date_list, frequency_list, 'b-', xdate=True)
    ax.plot_date(date_list, frequency_list ,'ro', xdate=True)
    plt.title('raw values')

def plot_lowpass(date_list, frequency_list):
    frequency_list_filtered = signal.lfilter(b, 10, frequency_list)    
    FC = 0.1#still need to find a good value here
    b = signal.firwin(len(frequency_list), cutoff=FC, window='hamming')    # filter numerator
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(date_list, frequency_list_filtered,'b-',xdate=True)
    ax.plot_date(date_list, frequency_list_filtered,'ro',xdate=True)
    plt.title('low pass filtered')


def plot_gauss(date_list, frequency_list):
    frequency_list_gauss = smoothListGaussian(frequency_list, False, 10)
    # frequency_list_gauss = smoothListGaussian(frequency_list)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    # ax.plot_date(date_list, frequency_list_gauss)
    ax.plot(frequency_list_gauss,'b-',)
    ax.plot(frequency_list_gauss,'ro',)
    plt.title('gauss filtered')

raw_data = get_data()
parsed_data = parse_data(raw_data)

if DEBUG:
    pprint.pprint (parsed_data)

date_list = [x['date']  for x in parsed_data]
frequency_list = [x['freq']  for x in parsed_data]

plot_raw(date_list, frequency_list)
plotSpectrum2(frequency_list,1)
plot_gauss(date_list, frequency_list)
plot_lowpass(date_list, frequency_list)

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
