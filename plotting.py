# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 20:57:46 2018

@author: brown

List of Modules:
       snr_plot:
              Plots range vs. snr
       propogation_plot:
              Plots range vs. propogation factor
       ant_pat:
              Plots antenna pattern as contour plot and 3D intensity plot
       rng_dop_map
              Plots radar returns in range vs doppler frequency
       waveform_plot:
              Plots radar waveform spectrum (power vs freq) and signal (power vs time)

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
    x1.set(xlabel = 'Range in meters', ylabel = 'SNR in dB', title = 'SNR vs. Range')
    plt.show()
    return

def propogation_plot(range_,F_db):
    f1 = plt.figure()
    x1 = f1.gca()
    p1 = x1.plot(range_,F_db)
    x1.set(xlabel = 'Range in meters', ylabel= 'Propogation Factor in dB', title = 'Range vs. Propogation Factor')
    plt.show()
    return

def rcs_plot(range_, sigma_db):
    f1 = plt.figure()
    x1 = f1.gca()
    sigma = convert.db2w(sigma_db)
    p1 = x1.plot(range_,sigma)
    plt.show()
    return

def gain_plot(range_,G):
    f1 = plt.figure()
    x1 = f1.gca()
    p1 = x1.plot(range_,G)
    plt.show()
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
    a1.set_title('Contour plot of pattern matrix')
    a1.set_xlabel('intensity per cell X (dB)')
    a1.set_ylabel('Intensity per cell Y (dB)')
    p2 = a2.plot_surface(X, Y, Z, cmap='plasma')
    a2.set(xlabel = 'Cell # X dimension', ylabel = 'Cell # Y dimension', title= '3D plot pattern')
    plt.show()
    return

def det_range():
        
    return

def rng_v_angle():
    
    return

def rng_dop_map():

    return


