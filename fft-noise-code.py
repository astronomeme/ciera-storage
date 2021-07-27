# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 10:50:53 2021

@author: naomi
"""

# imports ---------------------------------------------------------
# %matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import ascii
from astropy import constants as const

# start of fft -----------------------------------
# setting up values ------------------------------

filename1 = open('noise-output','r')
dummy1 = pd.read_csv('noise-output', delim_whitespace=False, comment='#', header=None)
#print(dummy1)

times = dummy1[0]
hps = dummy1[1]
hxs = dummy1[2]
tlist=[]
hplist = []
hxlist = []
for item in range(len((times))):
    if item!=0:
        tlist.append(eval(times[item]))
        hplist.append(eval(hps[item]))
        hxlist.append(eval(hxs[item]))
        
#print(hplist)

tsim = tlist[-1]
print(tsim)
npts = len(tlist)
dt = tsim / npts
print(dt)
 
        
# main fft code -------------------------------------

from scipy.fft import fft, ifft, fftfreq

hpfft = fft(hplist)
hxfft = fft(hxlist)

#print(hpfft)

#hpmax = hpfft.index(hpfft.max())
#hxmax = hxfft.index(hxfft.max())

#print(hpfft.max())

hpr = []
hpi = []

# for documentations sake
# it seems that the format for + and - versions
# is (some number at the front)
# then A-x, B-x
# then (some other number, not same as front)
# then B+x, A+x 

# getting complex conj, power -----------------------

hpconj = hpfft.conj()
hxconj = hxfft.conj()

hppower = hpfft * hpconj
hxpower = hxfft * hxconj
#print(hpfft)
#print('\n')
#print(hpconj)
#print('\n')
#print(hxpower)

# plotting with documentation --------------------

#x = np.linspace(0.0, npts*dt, npts, endpoint=False)
freqlist = fftfreq(npts, dt)[0:npts//2]
#print(freqlist)
freqsend = fftfreq(npts,dt)
#print(freqlist[hpmax])
#print(freqlist[hxmax])

#f,ax = plt.subplots(figsize=(8,5))
#ax.plot(freqlist,2.0/npts * hpfft[0:npts//2].real) #c='red', linewidths=0.3, edgecolors='k')
#ax.set_xlabel("freq")
#ax.set_ylabel("np fft real")

#f,ax = plt.subplots(figsize=(8,5))
#ax.plot(freqlist,2.0/npts * hxfft[0:npts//2].real)#c='red', linewidths=0.3, edgecolors='k')
#ax.set_xlabel("freq")
#ax.set_ylabel("nx fft real")

#f,ax = plt.subplots(figsize=(8,5))
#ax.plot(freqlist,2.0/npts * hpfft[0:npts//2].imag) #c='red', linewidths=0.3, edgecolors='k')
#ax.set_xlabel("freq")
#ax.set_ylabel("np fft imag")

#f,ax = plt.subplots(figsize=(8,5))
#ax.plot(freqlist,2.0/npts * hxfft[0:npts//2].imag)#c='red', linewidths=0.3, edgecolors='k')
#ax.set_xlabel("freq")
#ax.set_ylabel("nx fft imag")

f,ax = plt.subplots(figsize=(8,5))
ax.loglog(freqlist,2.0/npts * np.abs(hppower[0:npts//2])) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("log freq")
ax.set_ylabel("log hpn power")

f,ax = plt.subplots(figsize=(8,5))
ax.loglog(freqlist,2.0/npts * np.abs(hxpower[0:npts//2])) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("log freq")
ax.set_ylabel("log hxn power")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hppower[0:npts//2]) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hpn power")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hxpower[0:npts//2]) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hxn power")

# output info --------------------------------------

import csv
from  itertools import zip_longest
#with open('wahlquist-output', 'wb') as csv_file:
    #writer = csv.writer(csv_file, delimiter=',')
    #writer.writerow(['index','time','hp','hx'])
    #for i in range(0,len(indexprint)):
        #writer.writerow([indexprint[i],timeprint[i],hpprint[i],hxprint[i]])

# do i wanna send in all of my power lists
# or only the portion which i graphed?

d = [tlist,freqlist,hppower,hxpower]
export_data1 = zip_longest(*d,fillvalue = '')
with open('fft-noise-output', 'w',encoding="ISO-8859-1",newline='') as csv_file:
    wr = csv.writer(csv_file)
    wr.writerow(("time","freq","hpp","hxp"))
    wr.writerows(export_data1)
csv_file.close()
    



