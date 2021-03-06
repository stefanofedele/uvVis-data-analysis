# -*- coding: utf-8 -*-
"""
Created on Sun Mar 06 21:09:05 2016

@author: fedel_000
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#functions <------------------------------------------------------------------------------------
def sel(parameter, files): # select files according on the fact that the name includes "parameter"
    b = []
    for file_k in files:
        if parameter in file_k:
            b = b + [ file_k ]
    return b
    
def integTime(file_k): #find integral time
    index1 = file_k.find('integTime') + 9 
    index2 = file_k.find('Average') - 1
    return float( file_k[index1:index2].replace('_', '.') )
#functions <------------------------------------------------------------------------------------

path = r"C:\Users\fedel_000\Documents\Measurements\stefano\Reflectance_12_19_angle_resolved"
s = '\\' # '\\' for windows and '/' for linux
folders = os.listdir(path)
List = {} # dictionary of files by polarization
ListSG = {}
ListBG = {} # dictionary of backgrounds by polarization
#Angle = {}
reflectance = {}
j = 0 

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
ax.axis([400, 900, 0, 1])
Time = 1

for angles in folders:    
    print j       
    pathFiles = path + s + folders[j]
    listFiles = os.listdir(pathFiles)
    wavelength = pd.read_csv(pathFiles + s + listFiles[0], sep=',', header= None)[0].astype(float)    
    
    k = 0
    pol = ['noPol', '90Pol', '00Pol'] # different types of polarizations
    
    #for pol_k in pol:
    for pol_k in [ pol[2] ]: # it selects just one type of polarization
        List[ pol_k ] = sel( pol_k , listFiles) 
        ListBG[ pol_k ] = sel('background', List[ pol_k ])[0] # dictionary of backgrounds by polarizations            
        ListSG[ pol_k ] = sel( 'signal' , List[ pol_k ]) # dictionary of signals by polarization
        ListSG[ pol_k ] = sel( 'AuNR_angle' , ListSG[ pol_k ] ) # select spectra with ONLY Gold Nanorods
        
        #bg = pd.read_csv(pathFiles + s + ListBG[ pol[0] ], sep=',', header= None)[1].astype(float)/integTime( ListBG[ pol_k ] )        
        bg = pd.read_csv(pathFiles + s + ListBG[ pol_k ], sep=',', header= None)[1].astype(float)/integTime( ListBG[ pol_k ] )
        #set pol[0] on the previous line if you want all values normalized at the some background that is "noPol"
        for fileName in ListSG[ pol_k ]:    
            Path = pathFiles + s + fileName
            signal = pd.read_csv(Path, sep=',', header= None)[1].astype(float)/integTime(fileName)
            reflectance[ fileName ] = signal / bg
            line, = ax.plot(wavelength, reflectance[ fileName ], label = fileName[:-4])
            ax.legend(handles=[line])
            plt.pause(Time)
    
    j = j + 1


