# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:03:27 2021

@author: naomi
"""
# imports ---------------------------------------------------------
# %matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import ascii
from astropy import constants as const

# start of wahlquist ----------------------------------------------

# reading in to check ---------------------------------------------

filename1 = open('orbit-output','r')
dummy1 = pd.read_csv('orbit-output', delim_whitespace=False, comment='#', header=None)
#print(dummy1)

thetas = dummy1[4]
print(len(thetas))
times = dummy1[0]
print(len(times))
thetalist = []
tlist=[]
for item in range(len((thetas))):
    if item!=0:
        thetalist.append(eval(thetas[item]))
        tlist.append(eval(times[item]))
        
#thetalist.remove(thetalist[0])
#tlist.remove(tlist[0])
    
# reading in og file from shane and defining ---------------------------

filename = open('binarytwo.dat','r')
datalist = []
amcvn = filename.readlines()
amcvn
for item in amcvn:
    equals = item.index('=')
    datalist.append(item[equals+2:-1])
datalist

smajaxis = eval(datalist[1])
aumeter = 1.496 * (10**11)
smajaxis = smajaxis * aumeter

mass1 = eval(datalist[4])
mass2 = eval(datalist[5])
solarmass = 1.989 * (10**30)
mass1 = mass1 * solarmass
mass2 = mass2 * solarmass

g = const.G.value # already in SI

ecc = 0.5 #eval(datalist[2])

# constants and setting up -----------------------------------------

# starting the second part of the project
# mytime = 100 #the time we want to use >>> is this something shane gave me a default for?
mytheta = 0
#print(mytheta)

# any constant values
c = const.c.value
D = eval(datalist[6]) 
phi = eval(datalist[9])
inc = eval(datalist[3])
thetan = eval(datalist[7])
thetap = eval(datalist[8])

# to SI and radians
D = D * (3.0857 * (10**16))
phi = (phi * np.pi) / 180
inc = (inc * np.pi) / 180
thetan = (thetan * np.pi) / 180
thetap = (thetap * np.pi) / 180

# printing constants
#print("Constant c = " + str(c))
#print("Constant D = " + str(D))
#print("Constant phi = " + str(phi))
#print("Constant inc = " + str(inc))
#print("Constant thetan = " + str(thetan))
#print("Constant thetap = " + str(thetap))

# coefficient values
#print(g)

Hterm = smajaxis*(1-(ecc**2))
H = (4*(g**2)*mass1*mass2) / ((c**4)*Hterm*D)
A0 = -0.5 * (1+(np.cos(inc)**2)) * np.cos(2*(mytheta-thetan))
B0 = -1 * np.cos(inc) * np.sin(2*(mytheta-thetan))
A1 = (0.25 * (np.sin(inc)**2) * np.cos(mytheta-thetap)) - (0.125 * (1 + (np.cos(inc)**2)) * (5 * np.cos(mytheta-(2*thetan)+thetap) + np.cos((3*mytheta)-(2*thetan)-thetap)))
B1 = -0.25 * np.cos(inc) * (5 * np.sin(mytheta-(2*thetan)+thetap) + np.sin((3*mytheta)-(2*thetan)-thetap))
A2 = 0.25 * (np.sin(inc)**2) - 0.25 * (1+(np.cos(inc)**2)) * np.cos((2*thetan) - (2*thetap))
B2 = 0.5 * np.cos(inc) * np.sin((2*thetan) - (2*thetap))

# printing values
#print("H = " + str(H))
#print("A0 = " + str(A0))
#print("B0 = " + str(B0))
#print("A1 = " + str(A1))
#print("B1 = " + str(B1))
#print("A2 = " + str(A2))
#print("B2 = " + str(B2))

# that was writing it with just one theta value, given by the user
# presumably i need a loop to 
hplist = []
hxlist = []

for value in thetalist:
    
    #get theta and coeffs 
    mytheta = value
    A0 = -0.5 * (1+(np.cos(inc)**2)) * np.cos(2*(mytheta-thetan))
    B0 = -1 * np.cos(inc) * np.sin(2*(mytheta-thetan))
    A1 = (0.25 * (np.sin(inc)**2) * np.cos(mytheta-thetap)) - (0.125 * (1 + (np.cos(inc)**2)) * (5 * np.cos(mytheta-(2*thetan)+thetap) + np.cos((3*mytheta)-(2*thetan)-thetap)))
    B1 = -0.25 * np.cos(inc) * (5 * np.sin(mytheta-(2*thetan)+thetap) + np.sin((3*mytheta)-(2*thetan)-thetap))
    A2 = 0.25 * (np.sin(inc)**2) - 0.25 * (1+(np.cos(inc)**2)) * np.cos((2*thetan) - (2*thetap))
    B2 = 0.5 * np.cos(inc) * np.sin((2*thetan) - (2*thetap))
    
    # solve h equations
    
    # h plus
    hpfirst = (np.cos(2*phi)) * (A0 + (ecc*A1) + ((ecc**2)*A2))
    hpsecond = (np.sin(2*phi)) * (B0 + (ecc*B1) + ((ecc**2)*B2))
    hp = H * (hpfirst - hpsecond)
    hplist.append(hp)

    # h cross
    hxfirst = (np.sin(2*phi)) * (A0 + (ecc*A1) + ((ecc**2)*A2))
    hxsecond = (np.cos(2*phi)) * (B0 + (ecc*B1) + ((ecc**2)*B2))
    hx = H * (hxfirst + hxsecond)
    hxlist.append(hx)
    
#print(hplist)
#print('\n')
#print(hxlist)

# wahlquist plots --------------------------------------------------

# plot hp vs t, should look like sinusoid
f,ax = plt.subplots(figsize=(8,5))
ax.plot(tlist,hplist) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("time")
ax.set_ylabel("hp")

# plot hx vs t, should look like sinusoid
f,ax = plt.subplots(figsize=(8,5))
ax.plot(tlist,hxlist) #c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("time")
ax.set_ylabel("hx")

# output info --------------------------------------

import csv
from  itertools import zip_longest
#with open('wahlquist-output', 'wb') as csv_file:
    #writer = csv.writer(csv_file, delimiter=',')
    #writer.writerow(['index','time','hp','hx'])
    #for i in range(0,len(indexprint)):
        #writer.writerow([indexprint[i],timeprint[i],hpprint[i],hxprint[i]])

d = [tlist,hplist,hxlist]
export_data1 = zip_longest(*d,fillvalue = '')
with open('wahlquist-output', 'w',encoding="ISO-8859-1",newline='') as csv_file:
    wr = csv.writer(csv_file)
    wr.writerow(("time","hp","hx"))
    wr.writerows(export_data1)
csv_file.close()
    