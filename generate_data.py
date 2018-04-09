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