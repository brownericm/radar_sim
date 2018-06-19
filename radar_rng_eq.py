# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 20:51:54 2018

REMINDER!!
Keep vigilent for dot multipliers hidden in code a * b in matlab is a.dot(b) in numpy(matrix mult) a .* b is just a*b
REMINDER!!

NOTE!!!
IN PROGRESS: Add main() for radar sim
TODO: Refine RRE to take vector inputs and option plots
IN PROGRESS: Write plotting sub function
DONE: Implement PRFs
DONE: Write Range Res fn
DONE: Write Waveforms
DONE: Write Doppler fn
IN PROGRESS: Range and doppler ambiguity
TODO: CFAR
DONE: Add target data to radarparams (velocity vector, size(RCS), alt, etc)
DONE: Add Antenna pattern parsing (matlab to python)
TODO: Rewrite RRE for larger program
DONE: Double check sqrt() usage. np.sqrt and math.sqrt do not cast to complex automagically
    scipy.sqrt() is the correct one for this application
NOTE!!!

@author: Eric M Brown

@ref: B.R. Mahafza, Radar System Analysis and Design using MATLAB 3rd Edition
@ref: Richards, Fundamentals of Radar Signal Processing
@ref: Skolnik, Radar Handbook
"""
from envconst import c0, kb
from radarparams import  pt, BW, hr, To, NF, loss, freq
from scenario_setup import target_range, target_alt, target_rcs
from convert import w2db, db2w
import atmos_effects
from numpy import pi, linspace, log10, max, isscalar, broadcast_to, argmax
import plotting as plots

def RadarRngEq(G, beam_el, filename):
    """Prints SNR, will be modified for other uses later

    SNR = (pt*g^2*lambda_^2*sigma)/((4*pi)^3*k*temp_s*nf*l*r^4)
    pt = power transmitted - Watts
    freq = radar freq - Hz
    gain = antenna gain - db (default = 45)
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
#    snrplot = 1
#    propplot = 1
#    pat_plot = 1
#    rcsplot = 1
    gainplot = 0

    # Local Vars
    lambda_ = c0/freq #wavelength
    #beta = el_angle
    range_ = target_range
    ht = target_alt
    sigma = target_rcs
    F = atmos_effects.multipath(range_, ht, hr)


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
    tau_db = 10*log10(.2/12000)
    det_thresh = 13

    # Data Shaping
    if isscalar(G) is False:
           range_vec = linspace(2000, 100000, G.size) # for graphing
           G_vec = broadcast_to(G, (range_vec.size, G.size))
           range_vec = broadcast_to(range_vec, (range_vec.size, G.size))
    else:
           range_vec = linspace(2000, 250000, 1000)
    F_graph = atmos_effects.multipath(range_vec[0], ht, hr)
    F_graph = 4*w2db(0.0015+F_graph)

    #L_a = atmos_effects.atmo_absorp(ht, hr, freq, beta)

    # Radar Range Eq
    tx_db = pt_db + G + G + lambda_sqdb + sigma_db + F_db
    rx_db = four_pi_db + k_db + To_db + BW_db + NF + loss + range_db
    snr = tx_db - rx_db
    # TODO: Return to this
#    R_p = pt_db + gain + gain + lambda_sqdb + sigma_db + tau_db + F_graph + w2db(.01)
#    R_n = four_pi_db + k_db + To_db + NF + det_thresh
#    R_max = (R_p - R_n)**(1/4)
#    R_max = db2w(R_max)
    tx_db_graph = pt_db + G.max() + G.max() + lambda_sqdb + sigma_db + F_graph
    rx_db_graph = four_pi_db + k_db + To_db + BW_db + NF + loss + w2db(range_vec[0]**4)
    snr_graph = tx_db_graph.real - rx_db_graph
    tx_noF = pt_db + G.max() + G.max() + lambda_sqdb + sigma_db
    rx_noF = four_pi_db + k_db + To_db + BW_db + NF + loss + w2db(range_vec[0]**4)
    snr_noF = tx_noF - rx_noF

    print("The range at which your target first drops out due to multipath is " +
          str(range_vec[0][argmax(snr_graph < det_thresh)]) + " meters")


    # HACK: return all variable for viewing sanity check
    return snr_graph, range_, sigma_db, F_graph, range_vec, snr_noF
#RadarRngEq()
