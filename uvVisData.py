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

j = 0            
pathFiles = path + s + folders[j]
listFiles = os.listdir(pathFiles)

k = 0
pol = ['noPol', '90Pol', '00Pol'] # different types of polarizations
List = {} # dictionary of files by polarization
ListSG = {}
ListBG = {} # dictionary of backgrounds by polarization

for pol_k in pol:
    List[ pol_k ] = sel( pol_k , listFiles) 
    ListSG[ pol_k ] = sel( 'signal' , List[ pol_k ]) # dictionary of signals by polarization
    ListBG[ pol_k ] = sel('background', List[ pol_k ])[0] # dictionary of backgrounds by polarizations    
    for fileName in ListSG[ pol_k ]:    
        Path = pathFiles + s + fileName
        print pd.read_csv(Path, sep=',', header= None)[1].astype(float)/integTime(fileName)
    
