# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 20:57:46 2018

@author: brown

FIGURE OUT THE RIGHT WAY TO IMPLEMENT THIS
"""
import matplotlib.pyplot as plt

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
    #return x

def rng_dop_map():
    
    return


