# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 12:33:21 2021

@author: naomi
"""

# imports ---------------------------------------------------------
# %matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import ascii
from astropy import constants as const

# start of noise ----------------------------------------------

# reading in to check ---------------------------------------------

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

filename = open('binarytwo.dat','r')
datalist = []
amcvn = filename.readlines()
amcvn
for item in amcvn:
    equals = item.index('=')
    datalist.append(item[equals+2:-1])
    
# getting into the code ------------------------------

variance = 2.0 * (10**-20) # ^-23? dont remember. eq to sd, sig.
rho = 10 #0.05 # anything in particular? 
maxhp = np.amax(hplist)
maxhx = np.amax(hxlist)
scalehp = maxhp / rho
scalehx = maxhx / rho
#unscaled1 = np.random.normal(variance,rho,len(tlist))
#unscaled2 = np.random.normal(variance,rho,len(tlist))
unscaled1 = np.random.normal(0.0,1.0,len(tlist)) 
unscaled2 = np.random.normal(0.0,1.0,len(tlist)) 
# thing is, this seems to be in the wrong order
# it should be mean then sd according to doc
# which means my values might be backwards?
noiselisthp = []
noiselisthx = []

for index in range(0,len(tlist)):
    basenoisehp = unscaled1[index]
    basenoisehx = unscaled2[index]
    truenoisehp = scalehp * basenoisehp
    truenoisehx = scalehx * basenoisehx
    noiselisthp.append(truenoisehp)
    noiselisthx.append(truenoisehx)
    
# addings signals ----------------------------

signalhp = np.array(noiselisthp) + np.array(hplist)
signalhx = np.array(noiselisthx) + np.array(hxlist)

# graphing to test -------------------------------------
    
f,ax = plt.subplots(figsize=(8,5))
ax.plot(tlist,noiselisthp)
ax.set_xlabel("time")
ax.set_ylabel("hp noise")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(tlist,noiselisthx)
ax.set_xlabel("time")
ax.set_ylabel("hx noise")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(tlist,signalhp)
ax.set_xlabel("time")
ax.set_ylabel("hp signal + noise")

f,ax = plt.subplots(figsize=(8,5))
ax.plot(tlist,signalhx)
ax.set_xlabel("time")
ax.set_ylabel("hx signal + noise")

# write to file ----------------------------------------

import csv
from  itertools import zip_longest

d = [tlist,signalhp,signalhx]
export_data1 = zip_longest(*d,fillvalue = '')
with open('data-output', 'w',encoding="ISO-8859-1",newline='') as csv_file:
    wr = csv.writer(csv_file)
    wr.writerow(("time","signalhp","signalhx"))
    wr.writerows(export_data1)
csv_file.close()

d2 = [tlist,noiselisthp,noiselisthx]
export_data2 = zip_longest(*d2,fillvalue = '')
with open('noise-output', 'w',encoding="ISO-8859-1",newline='') as csv_file:
    wr = csv.writer(csv_file)
    wr.writerow(("time","noiselisthp","noiselisthx"))
    wr.writerows(export_data2)
csv_file.close()