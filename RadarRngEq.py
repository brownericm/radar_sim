# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 20:51:54 2018

REMINDER!!
Keep vigilent for dot multipliers hidden in code a * b in matlab is a.dot(b) in numpy(matrix mult) a .* b is just a*b
REMINDER!!

NOTE!!!
TODO: Add main() for radar sim
TODO: Refine RRE to take vector inputs and option plots
TODO: Write plotting sub function
TODO: Implement PRFs
TODO: Write Range Res fn
TODO: Write Waveforms
TODO: Write Doppler fn
TODO: Range and doppler ambiguity
TODO: CFAR
TODO: Add target data to radarparams (velocity vector, size(RCS), alt, etc)
TODO: Add Antenna pattern parsing (matlab to python)
TODO: Rewrite RRE for larger program
TODO: Double check sqrt() usage. np.sqrt and math.sqrt do not cast to complex automagically
    scipy.sqrt() is the correct one for this application
NOTE!!!

@author: Eric M Brown

@ref: B.R. Mahafza, Radar System Analysis and Design using MATLAB 3rd Edition
@ref: Richards, Fundamentals of Radar Signal Processing
@ref: Skolnik, Radar Handbook
"""
from envconst import c0, kb
from radarparams import el_angle, pt, BW, range_, ht, hr, To, sigma, NF, G, loss, freq
from convert import w2db
import atmos_effects
from numpy import pi
import plotting as plots
import matplotlib.pyplot as plt

def RadarRngEq():
    """Prints SNR, will be modified for other uses later

    SNR = (pt*g^2*lambda_^2*sigma)/((4*pi)^3*k*temp_s*nf*l*r^4)
    pt = power transmitted - Watts
    freq = radar freq - Hz
    G = antenna gain - db
    sigma = RCS - m^2
    BW = bandwidth - Hz
    NF = noisefigure dB
    loss = radar losses dB
    range = Km
    snr = dB

    MOST OF THESE WILL BE MADE TO BE F_N INPUTS FOR NOW THIS IS
    FROM RADARPARAMS
    """
    #######################
    #   TOGGLE PLOTTING   #
    #######################
    snrplot = 1
    propplot = 1
    rcsplot = 0
    gainplot = 0

    # Local Vars
    lambda_ = c0/freq #wavelength
    beta = el_angle

    # Propogation Effects
    F = atmos_effects.multipath(range_, ht, hr)
    #L_a = atmos_effects.atmo_absorp(ht, hr, freq, beta)

    # dB Conversions
    lambda_sqdb = w2db(lambda_**2)
    pt_db = w2db(pt) #peak power in dB
    k_db = w2db(kb)
    sigma_db = w2db(sigma)
    To_db = w2db(To)
    BW_db = w2db(BW)
    range_db = w2db(range_**4)
    four_pi_db = w2db((4*pi)**3)
    F_db = 4 * w2db(0.0015+F)


    # Radar Range Eq
    tx_db = pt_db + G + G + lambda_sqdb + sigma_db + F_db
    rx_db = four_pi_db + k_db + To_db + BW_db + NF + loss + range_db

    snr = tx_db - rx_db
    if snrplot == True:
        plt.plot(range_,snr, '-')
        plt.plot()
        plt.show()

    if propplot == True:
        plots.propogation_plot(range_,F_db)
        plt.show()

    # return all variable for viewing sanity check
    return F_db, pt_db, lambda_sqdb, k_db, sigma_db, To_db, BW_db, range_db, four_pi_db
F_dB, pt_db, lambda_sqdb, k_db, sigma_db, to_db, b_db, range_db, four_pi_db = RadarRngEq()
