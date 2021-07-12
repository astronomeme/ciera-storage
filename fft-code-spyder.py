# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:56:18 2021

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

filename1 = open('wahlquist-output','r')
dummy1 = pd.read_csv('wahlquist-output', delim_whitespace=False, comment='#', header=None)
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

print(hpfft)

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
print(freqlist)
#print(freqlist[hpmax])
#print(freqlist[hxmax])

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hpfft[0:npts//2].real) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hp fft real")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hxfft[0:npts//2].real)#c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hx fft real")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hpfft[0:npts//2].imag) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hp fft imag")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hxfft[0:npts//2].imag)#c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hx fft imag")

#f,ax = plt.subplots(figsize=(8,5))
#ax.loglog(freqlist,2.0/npts * np.abs(hxfft[0:npts//2])) #c='red', linewidths=0.3, edgecolors='k')
#ax.set_xlabel("log freq")
#ax.set_ylabel("log hx fft")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hppower[0:npts//2]) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hp power")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(freqlist,2.0/npts * hxpower[0:npts//2]) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hx power")





