# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 16:03:01 2018

@author: brown

This file generates the raw datacube for the targets. Any loops
should be vectorized ASAP for performance

##########
## PLAN ##
##########

For each PRF we need to iterate 0:(CPI-1) b/c of zero indexing:

       Set up fast time axes The range window is 0 : max range
       set # of range bins and preallocate a vector
       preallocate vector for return pulse data
       iterate over number of pulse rep intervals:
              set time
              iterate over targets:
                     get range @ start + time
                     pull pulse from radar params and apply doppler spread, time delay, target return power scaling
                     apply antenna off-boresight scaling
                     place pulse into data matrix and continue to next pulse
              Add noise and clutter to pulse matrix
       step in CPI time
       write pulse info to scenario data structure

"""
from envconst import c0, kb
from radarparams import  pt, BW, hr, To, NF, loss, freq, ncpi, npri, nfft, PRF
from scenario_setup import target_range, target_alt, target_rcs, target_radvel
from convert import w2db # db2w
import atmos_effects
from numpy import pi, log10 #max, isscalar, broadcast_to, argmax
import scipy as sp
import radarparams as rp

class StructType: # pass through class for structs
    pass

def calc_rcv_pow(G = 45, beam_el = None):
    """
       This module replaces radar_rng_eq.py and functionizes its outputs.
       Extra bits of the rng_eq file that are not SNR calcs will be moved to the wrapper file
       i.e. plotting toggles, local variables, todo lists and references.
       """
    # Local Vars
    lambda_ = c0 / freq  # wavelength
    # beta = el_angle
    range_ = target_range
    ht = target_alt
    sigma = target_rcs
    F = atmos_effects.multipath(range_, ht, hr)

    # dB Conversions
    lambda_sqdb = w2db(lambda_ ** 2)
    pt_db = w2db(pt)  # peak power in dB
    k_db = w2db(kb)
    sigma_db = w2db(sigma)
    To_db = w2db(To)
    BW_db = w2db(BW)
    range_db = w2db(range_ ** 4)
    four_pi_db = w2db((4 * pi) ** 3)
    F_db = 4 * w2db(0.0015 + F)
    tau_db = 10 * log10(.2 / 12000)
    det_thresh = 13
    """
    # Data Shaping
    if isscalar(G) is False:
        range_vec = linspace(2000, 100000, G.size)  # for graphing
        G_vec = broadcast_to(G, (range_vec.size, G.size))
        range_vec = broadcast_to(range_vec, (range_vec.size, G.size))
    else:
        range_vec = linspace(2000, 250000, 1000)
    F_graph = atmos_effects.multipath(range_vec[0], ht, hr)
    F_graph = 4 * w2db(0.0015 + F_graph)

    # L_a = atmos_effects.atmo_absorp(ht, hr, freq, beta)
"""
    # Radar Range Eq
    tx_db = pt_db + G + G + lambda_sqdb + sigma_db + F_db
    rx_db = four_pi_db + k_db + To_db + BW_db + NF + loss + range_db
    snr = tx_db - rx_db
    print("Received power is " + rx_db + " and SNR is " + snr)
    return rx_db
"""
    # TODO: Return to this
    #    R_p = pt_db + G + G + lambda_sqdb + sigma_db + tau_db + F_graph + w2db(.01)
    #    R_n = four_pi_db + k_db + To_db + NF + det_thresh
    #    R_max = (R_p - R_n)**(1/4)
    #    R_max = db2w(R_max)
    
    tx_db_graph = pt_db + G.max() + G.max() + lambda_sqdb + sigma_db + F_graph
    rx_db_graph = four_pi_db + k_db + To_db + BW_db + NF + loss + w2db(range_vec[0] ** 4)
    snr_graph = tx_db_graph.real - rx_db_graph
    tx_noF = pt_db + G.max() + G.max() + lambda_sqdb + sigma_db
    rx_noF = four_pi_db + k_db + To_db + BW_db + NF + loss + w2db(range_vec[0] ** 4)
    snr_noF = tx_noF - rx_noF
    """

def gen_data():
    cpi_start = 0
    for i in range(1, ncpi):
        '''
        This will loop to create data for each CPI, the first section will
        create vectors for the radar attributes that aligns with the data 
        it is collected from
        '''
        prf = PRF  # will become vector
        range_unam = c0/prf/2
        tcpi = 1/prf
        rng_window = sp.ndarray([0, range_unam])
        fast_time = rng_window/c0*2
        ft_axis = sp.arange(fast_time[0], fast_time[1], 1/(2*BW))
        numbins = ft_axis.size
        rng_axis = sp.linspace(0, numbins, rng_window[1])
        p_data = sp.zeros((numbins, npri))
        for p in range(1,npri):
            time = (p-1)*tcpi
            # itarget in range(0,len(target_range)): # this when I get to multiple targets
            range_new = target_range + target_radvel
            tmp_array = calc_rcv_pow() * rp.pulse * sp.exp(
                sp.sqrt(-1)*2*pi*( sp.arange(0, len(rp.pulse)-1)/rp.fs+time) * 2 * target_radvel/(c0/freq) )
            '''
            Insert generated data into appropriate 'bins'
            Each i loop goes into it's own MxN matrix and is stacked in a 3rd dim
            making it (rng x dop x cpi). The tmp_array calculates the value of the target
            while the indexing below slots it into the correct dopper bins. The range binning is taken care of by the 
            the pri loop.
            '''
            index1 = round(sp.mod(range_new, rng_window[1]/(rng_window[1]*(numbins-1))+1))
            index2 = index1 + min(len(rp.ts-1), numbins-index1)
            index_size = sp.arange(index1, index2+1)
            rev_tmp = tmp_array[0:index_size]
            p_data[p, index_size = p_data[p, index_size] + rev_tmp[:: -1]
        cpi_start = cpi_start + time + tcpi + 1/rp.fs
        '''
        sort the data into a structure of some kind
        '''
        data = structType
        data = sp.array([p_data], dtype )


