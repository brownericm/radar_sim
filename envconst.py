# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:39:30 2018

@author: brown
"""
from numpy import array, pi

c0 = 299792458
kb = 1.3806503e-23
r2d = 180/pi
d2r = pi/180
r0 = 6.375E3
re = r0*(4/3)

# selection of reflection surface values and corresponding ce in km [N0n, cen]
# US average is N0=313
N0 = array([[200, 0.1184], [250, 0.1256], [301, 0.1396], [313, 0.1439], [400, 0.1867], [450, 0.2233]])

# wvd[0] = height in km; wvd[1] = water vapor density 
wvd =  array([[0.00000000e+00, 6.18000000e+00],
       [7.62000000e-01, 4.93000000e+00],
       [1.52400000e+00, 3.74000000e+00],
       [3.04800000e+00, 2.01000000e+00],
       [6.09600000e+00, 3.40000000e-02],
       [9.14400000e+00, 5.00000000e-03],
       [1.21920000e+01, 2.22044605e-16],
       [1.31920000e+01, 2.22044605e-16]])
