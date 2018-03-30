# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 20:57:46 2018

@author: brown

FIGURE OUT THE RIGHT WAY TO IMPLEMENT THIS
"""
import matplotlib.pyplot as plt

def snr_plot(range_,snr):
    #fig = plt.figure()
    x = plt.plot(range_,snr)
    return x

def propogation_plot(range_,F_db):
    plt.plot(range_,F_db)
    plt.show()
    #return x

def rcs_plot(range_, sigma_db):
    plt.plot(range_, sigma_db)
    #return x


