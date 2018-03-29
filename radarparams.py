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
 # Variables
pt = 1.5E+6
freq = 5.6E+9
g = 45
b = 5E+6
nf = 3
loss = 6
sigma = 0.1
range_ = 25e+3
to = 290 #temp
range_max = 250000
ht = 30.48 * 2
hr = 30.48
