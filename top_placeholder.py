# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 06:19:04 2018

@author: brown

This is a placeholder for whatever I name the driver file. This will manage the timings
of all the various aspects of the simulation and call the functions that give the outputs.

I expect there will be many toggles for plotting and data variations, and some way to
manage the final pulse return data structure and sub arrays.
"""
import scipy as sp
import scipy.io as sio
import radar_rng_eq as rre
import matplotlib.pyplot as plt
import plotting as plots

#############################################
# PLEASE INPUT THESE ITEMS FROM YOUR DESIGN #
#############################################
# My beam patter will no longer be loaded by default, you MUST declare a filename

beam_el = 15 # at what theta did you  place the boresight?
filename = 'a.mat' # with or without the file extension this should still work
var = '<YOUR MATLAB VARIABLE NAME HERE>' # Use the name that was used in MATLAB

#######################
#   TOGGLE PLOTTING   #
#######################
# TODO: Make plotting options into list before passing
snrplot = 1
propplot = 1
pat_plot = 1
rcsplot = 1
# gainplot = 0
# detrng = 1
# rng_angle = 1

######################
##    FUNCTIONS     ##
######################

def load_pat(filename):
#    if filename is None:
#        file = sio.loadmat('a.mat')
#        file_pat = file[list(file.keys())[3]]
#    else:
    file = sio.loadmat(filename)
    file_pat = file[var]
    return file_pat
pattern = load_pat(filename)
max_G = pattern.max()

#find maximal cut axes (row,colum)
ind = sp.unravel_index(sp.argmax(pattern, axis=None), pattern.shape)
#G_az = sp.reshape(pattern[ind[0]], (1,pattern[ind[0]].size))
G_el = sp.reshape(pattern[ind[1]], (1,pattern[ind[1]].size))


#R_max_az = rre.RadarRngEq(G_az)
snr_graph, range_, sigma_db, F_graph, range_vec, snr_noF = rre.RadarRngEq(G_el, beam_el, filename)


#########
# PLOTS #
########
if snrplot == True:
    # HACK: I want to show standard plots for students while still developing the more sophisticated scenario
    plots.snr_plot(range_vec[0],snr_graph, snr_noF)
    #plots.snr_plot(range_vec[0],snr_noF)

if propplot == True:
    # HACK: I want to show standard plots for students while still developing the more sophisticated scenario
    plots.propogation_plot(range_vec[0],F_graph.real)

if rcsplot is True:
    plots.rcs_plot(range_,sigma_db)



if pat_plot == True:
    plots.ant_pat(pattern)

#    if detrng is True:
#        plots.det_range()


#X_el = sp.arange(0,G_el.size,1)
#r1 = plt.figure()
#x1 = r1.gca()
#p1 = x1.plot(X_el,R_max_el)
#p1.xticks(sp.arange(-90,91,1))
#plt.show()

