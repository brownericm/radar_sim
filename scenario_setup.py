# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 17:38:37 2018

@author: brown
TODO: This needs to be turned into a struct so data can be efficiently passed and updated btw modules
TODO: Impliment dynamic scenario with true lat/long basis for target and platform
"""
# HACK: Static target for rng_dop_map development process
# Approx Su-30MKI specs at cruising speed
target_vel = 600 # kph
target_bearing = 20 # deg
target_pitch = 0 # deg
target_alt = 2 # km
target_rcs = 4 # m2
#target_type = swerling1 # swerling type (1,2,3,4)
