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
import scipy as sp
import envconst as env
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

# Pulse Parameters
ncpi = 10 # number of coherent processing intervals
npri = 50 # number of pulses per interval (range bins)
nfft = 50 # number of doppler bins
PRF = 12000 #Hz (for now just a single PRF)

# TODO: make pulse type a class
pulse_type = 'lfm' # pulse type right now can be either instantaneous (None) or lfm

if pulse_type is 'lfm':
       duty = .2
       freq1 = 10E+9
       freq2 = 10E+9 + 5E+6
       BW = freq2-freq1
       tau = duty/PRF

       # Time Bandwidth Product
       tbp = tau*BW

       # Sampling Rate
       fs = 2*BW

       # LFM Pulse (up/down)
       ts = sp.arange(-tau/2, tau/2, 1/freq)
       ramp = np.pi*BW/tau
       pulse = sp.exp(1j*ramp*ts**2)

# Gating and RDMap Axes
range_res = env.c0/2/BW
range_axis = sp.arange(0, range_max, range_res)
range_unambig= env.c0/PRF/2
num_rngbins = sp.ceil(range_max/range_res)

# TODO: when additional PRF added come back and make doppler_res sp.maximum(PRF)/nfft
doppler_res = PRF/nfft 
doppler_max = PRF/2 # unfold doppler space N times N*PRF/2
doppler_axis = sp.arange(-doppler_max, doppler_max, doppler_res)
num_dopbins = doppler_axis.size




