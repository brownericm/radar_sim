# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 20:51:54 2018

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

NOTE!!!

@author: Eric M Brown

@ref: B.R. Mahafza, Radar System Analysis and Design using MATLAB 3rd Edition
@ref: Richards, Fundamentals of Radar Signal Processing
@ref: Skolnik, Radar Handbook
"""

import EnvConst as env
import radarparams as rp
import convert as con
import math as M
import atmos_effects

def RadarRngEq():
    """Prints SNR, will be modified for other uses later

    SNR = (pt*g^2*lambda_^2*sigma)/((4*pi)^3*k*temp_s*nf*l*r^4)
    pt = power transmitted - Watts
    freq = radar freq - Hz
    g = antenna gain - db
    sigma = RCS - m^2
    b = bandwidth - Hz
    nf = noisefigure dB
    loss = radar losses dB
    range = Km
    snr = dB

    MOST OF THESE WILL BE MADE TO BE F_N INPUTS FOR NOW THIS IS
    FROM RADARPARAMS
    """
    # Local Vars
    lambda_ = env.c0/rp.freq #wavelength

    # Stuff

    F = atmos_effects.multipath(rp.range_, rp.ht, rp.hr)
    # dB Conversions
    pt_db = con.w2db(rp.pt) #peak power in dB
    lambda_sqdb = con.w2db(lambda_**2)
    k_db = con.w2db(env.kb)
    sigma_db = con.w2db(rp.sigma)
    to_db = con.w2db(rp.to)
    b_db = con.w2db(rp.b)
    range_db = con.w2db(rp.range_**4)
    four_pi_db = con.w2db((4*M.pi)**3)
    F_dB = 4 * con.w2db(0.0015+F)


    # Radar Range Eq
    tx_db = pt_db + rp.g +rp.g + lambda_sqdb + sigma_db + F_dB
    rx_db = four_pi_db + k_db + to_db + b_db + rp.nf + rp.loss + range_db
    snr = tx_db - rx_db

    print(snr)

    # return all variable for viewing sanity check
    return F_dB, pt_db, lambda_sqdb, k_db, sigma_db, to_db, b_db, range_db, four_pi_db

F_dB, pt_db, lambda_sqdb, k_db, sigma_db, to_db, b_db, range_db, four_pi_db = RadarRngEq()