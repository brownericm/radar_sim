# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:27:55 2018

@author: brown

    pt = power transmitted - Watts
    freq = radar freq - Hz
    g = antenna gain - db
    sigma = RCS - m^2
    b = bandwidth - Hz
    nf = noisefigure dB
    loss = radar losses dB
    range_ = m
    snr = dB

    MOST OF THESE WILL BE MADE TO BE F_N INPUTS

"""
# Booleans
"""
Not implements yet but make booleans for various effects to turn on off
divergence = 1
atmo_attn = 0
etc...
Then at multipath or radarrngeq have the method check boolean to determine if
we are calculating that effect
"""
import numpy as np
 # Variables
pt = 1.5E+6
freq = 3E+9
G = 45
BW = 5E+6
NF = 3
loss = 6
To = 290 #temp
range_max = 250000
hr = 30.48

# TARGET INFO
ht = 30.48 * 2
range_ = np.linspace(2000, 55000, 500)
sigma = 0.1
el_angle = 10