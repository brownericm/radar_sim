# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 17:38:37 2018

@author: brown
TODO: This needs to be turned into a struct so data can be efficiently passed and updated btw modules
TODO: Impliment dynamic scenario with true lat/long basis for target and platform
"""
# HACK: Static target for rng_dop_map development process
target_radvel = 320 # m/s
target_el_angel = 10 # deg
target_pitch = 0 # deg
target_alt = 30.48 * 2 # m
target_rcs = .1 # m2
target_range = 100E3 #km
#target_type = swerling1 # swerling type (1,2,3,4)
