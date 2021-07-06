# -*- coding: utf-8 -*-
"""
Orbit and Wahlquist Code
( to be seperated later )

"""

# imports ----------------------------------------------------------
# %matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import ascii
from astropy import constants as const

# functions ---------------------------------------------------------

def keqn(manomaly,psi):
    kep = psi- (ecc*np.sin(psi)) - manomaly
    return kep

def shapeq(rp,theta):
    r = (rp*(1+ecc)) / (1 + ecc*np.cos(theta))
    return r

def bisec(psihigh,psilow,bimanom):
    
    khigh = keqn(bimanom,psihigh)
    klow = keqn(bimanom,psilow)
    tolerance = 0.00001
    
    psinew = psilow + (0.5*(psihigh-psilow))
    knew = keqn(bimanom,psinew)
    
    if np.sign(klow) > 0 or np.sign(khigh) < 0:
        string = "No Root Possible!"
        return string
    
    while(abs(knew) >= tolerance):
        if np.sign(knew) > 0:
            psihigh = psinew
            #print('down')
        elif np.sign(knew) < 0:
            psilow = psinew
            #print('up')
        psinew = psilow + (0.5*(psihigh-psilow))
        knew = keqn(bimanom,psinew)
        
    if knew < tolerance:
        return psinew
    
# reading  ------------------------------------------------------

filename = open('binarytwo.dat','r')
datalist = []
amcvn = filename.readlines()
amcvn
for item in amcvn:
    equals = item.index('=')
    datalist.append(item[equals+2:-1])
datalist

# init cons ------------------------------------------------------

tsim = eval(datalist[11]) #= 6.16 * (10**-5)
tsim = tsim * (3.15*(10**7))
#print(tsim)

#masses, switching to SI units aka kg
mass1 = eval(datalist[4])
mass2 = eval(datalist[5])
solarmass = 1.989 * (10**30)
mass1 = mass1 * solarmass
mass2 = mass2 * solarmass
#print(mass1)
#print(mass2)

#semi-major axis
smajaxis = eval(datalist[1])
aumeter = 1.496 * (10**11)
smajaxis = smajaxis * aumeter
#print(smajaxis)

#eccentricity 
ecc = eval(datalist[2])
#print(ecc)

#orbital period
g = const.G.value # already in SI
#print(g)
initnumer = 4 * (np.pi**2) * (smajaxis**3)
initdenom = (mass1 + mass2) * g
P = np.sqrt(initnumer/initdenom)
#print(P)

#rp, for later
rp = smajaxis * (1-ecc)
#print(rp)

# the low and high can be found in the file
# can steps be found in the file?
# used variables so i can always edit my times array

low = 0
high = 10000
step = eval(datalist[12])
timeindex = np.linspace(low,tsim,step)
dt = tsim / step
#dt = datalist[11] / step
#print(timeindex)
#print(dt)

# main orbit code --------------------------------------------------

# create list that will hold my thetas for each time, maybe by r values too
thetalist = []
rlist = []
xlist = []
ylist = []
plist = []
tlist=[]
currentime = 0
psihi = 1000
psilo = 0
deltapsi = 2

for item in timeindex: 
    # if dt is the step in timeindex
    # then i dont even need to do in range steps
    # i can just do it for each item in the timeindex since that'll change to the correct time each time
    
    currentime = item
    tlist.append(currentime)
    manom = ((2*np.pi)/P)*currentime
     
    # i define my bracket somewhere here
    psirt = bisec(psihi,psilo,manom)
    plist.append(psirt)
    numer = 1+ecc
    denom = 1-ecc
    squareroot = np.sqrt(numer/denom)
    theta = 2*(np.arctan(squareroot*np.tan(psirt/2))) #+ (loop*np.pi)
    #theta = (theta * 180) / np.pi #putting into degrees for SI
    
    #adding to my lists
    thetalist.append(theta)
    rlist.append(shapeq(rp,theta))
    xlist.append(shapeq(rp,theta) * np.cos(theta))
    ylist.append(shapeq(rp,theta) * np.sin(theta))
    
    psihi = psilo + deltapsi
    psilo = psirt
    #currentime = ((P*manom) / (2*np.pi))
    #currentime = currentime + dt
    
# orbit plots ------------------------------------------------

#plotting my orbit
f,ax = plt.subplots(figsize=(8,5))
ax.scatter(xlist,ylist, c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("x(m)")
ax.set_ylabel("y(m)")
#ax.set_aspect('equal') #command for to check if it looks right / equal aspect ratio
#ax.set_xlim(-3*(10**8),5*(10**7))
#ax.set_ylim(-3*(10**8),5*(10**8))

f,ax = plt.subplots(figsize=(8,5))
ax.scatter(tlist,plist, c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("time")
ax.set_ylabel("psi")

f,ax = plt.subplots(figsize=(8,5))
ax.scatter(tlist,thetalist, c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("t")
ax.set_ylabel("theta")

f,ax = plt.subplots(figsize=(8,5))
ax.scatter(tlist,xlist, c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("time")
ax.set_ylabel("x")

f,ax = plt.subplots(figsize=(8,5))
ax.scatter(tlist,ylist, c='red', linewidths=0.3, edgecolors='k')
ax.set_xlabel("time")
ax.set_ylabel("y")

# orbit file output -----------------------------------------------

import csv
from  itertools import zip_longest
#with open('wahlquist-output', 'wb') as csv_file:
    #writer = csv.writer(csv_file, delimiter=',')
    #writer.writerow(['index','time','hp','hx'])
    #for i in range(0,len(indexprint)):
        #writer.writerow([indexprint[i],timeprint[i],hpprint[i],hxprint[i]])

d = [tlist,xlist,ylist,rlist,thetalist]
export_data1 = zip_longest(*d,fillvalue = '')
with open('orbit-output', 'w',encoding="ISO-8859-1",newline='') as csv_file:
    wr = csv.writer(csv_file)
    wr.writerow(("time","x","y","r","theta"))
    wr.writerows(export_data1)
csv_file.close()