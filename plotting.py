# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 20:57:46 2018

@author: brown

FIGURE OUT THE RIGHT WAY TO IMPLEMENT THIS
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import convert
import scipy.io as sio

def snr_plot(range_,snr):
    f1 = plt.figure()
    x1 = f1.gca()
    p1 = x1.plot(range_,snr)
    plt.show()
    return

def propogation_plot(range_,F_db):
    f1 = plt.figure()
    x1 = f1.gca()
    p1 = x1.plot(range_,F_db)
    plt.show()
    return

def rcs_plot(range_, sigma_db):
    plt.plot(range_, sigma_db)
    return 

def ant_pat(filename = None):
    """
    !!! FOR ENGIN 465 !!!
    In order to plot your array pattern, save the pattern file in your radar_sim folder. Pass the filename into the plotting call in radar_rng_eq
    as ant_pat(filename= '<filename.mat>') where the letters inside the <> are your pattern file.
    My circular array pattern is in the folder as an example. It is also the default
    Remember to convert to dB either in MATLAB or use convert.w2db(<your_imported_pattern>)
    """
    if filename is None:
        file = sio.loadmat('51by51_circ_pat_db.mat')
        file_pat = file['pattern'] 
        
    else:
        file = sio.loadmat(filename)
    
    file_pat = file['pattern'] 
    
    # Set up dimension for graphing
    dim = np.shape(file_pat)
    X = np.arange(0,dim[0])
    Y = np.arange(0,dim[1])
    X, Y = np.meshgrid(X, Y)
    Z = file_pat
    
    # Plot
    f1 = plt.figure()
    a1 = plt.subplot(2,1,1)
    a2 = plt.subplot(2,1,2,projection='3d')
    
    p1 = a1.contour(file_pat)
    p2 = a2.plot_surface(X, Y, Z, cmap='plasma')
    plt.show()
    return

def rng_dop_map():
    
    return


