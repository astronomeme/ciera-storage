# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 10:51:55 2021

@author: naomi
"""

#imports -------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import ascii
from astropy import constants as const

#setting up -------------------------------------------------

filename1 = open('fft-noise-output','r')
dummy = pd.read_csv('fft-noise-output', delim_whitespace=False, comment='#', header=None)

times = dummy[0]
freq = dummy[1]
hpp = dummy[2]
hxp = dummy[3]
tlist=[]
freqlist = []
hppower = []
hxpower = []
for item in range(len((times))):
    if item!=0:
        tlist.append(eval(times[item]))
        freqlist.append(freq[item])
        hppower.append(eval(hpp[item]))
        hxpower.append(eval(hxp[item]))
        
tsim = tlist[-1]
npts = len(tlist)
dt = tsim / npts
df = 1/tsim
#print(df)


# only using the positive frequencies
#which means i need to change dimensions of the other array?
freqlist = freqlist[1:(npts//2)]
hppower = hppower[1:(npts//2)]
hxpower = hxpower[1:(npts//2)]
# all have a length of 511
# since i cut out the dc case
# running from 1 of og array to 512 of og array
# highest indexable term is [510] because of this

# harmonic correlation code -------------------------------
# REMEMBER f2 IS THE INDEX 1 ITEM IN FREQLIST

hphclist = [] #list of hc for each freq
hxhclist = []


for index in range(0,len(freqlist)): #from 0 to 510 
    current = index
    k = 2 #number of harmonics to get 
    harmlist = []
    hpmults = 1
    hxmults = 1
    for loop in range(1,k+1): # so loop != 0
        harmindex = loop * current
        #if harmindex>len(freqlist):
            #break
        harmlist.append(harmindex)
    print(harmlist)
    for term in harmlist:
        if term > len(freqlist)-1: #len(freqlist)//k
            hpmults = 0 
            hxmults = 0 
            break
        hp = hppower[term]
        hx = hxpower[term]
        hpmults = hpmults * hp
        hxmults = hxmults * hx
    hphclist.append(hpmults)
    hxhclist.append(hxmults) 

# no more str ---------------------------------------------

formatfreq = []
for each in freqlist:
    item = float(each)
    formatfreq.append(item)
    
# graphing --------------------------------------------

from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter
from matplotlib import ticker

f,ax = plt.subplots(figsize=(8,5))
ax.loglog(formatfreq,2.0/npts * np.abs(hphclist[0:npts//2])) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("log freq")
ax.set_ylabel("log hpn hc")

f,ax = plt.subplots(figsize=(8,5))
ax.loglog(formatfreq,2.0/npts * np.abs(hxhclist[0:npts//2])) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("log freq")
ax.set_ylabel("log hxn hc")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(formatfreq,hphclist)
ax.set_xlabel("freq")
ax.set_ylabel("hpn hc")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(formatfreq,hxhclist) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("freq")
ax.set_ylabel("hxn hc")

#ax.plot(freqlist[:1023],hphclist)
