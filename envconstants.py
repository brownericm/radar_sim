# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:39:30 2018

@author: brown
"""
from numpy import array

c0 = 299792458
kb = 1.3806503e-23
earth_r0 = 6375E3
earth_re = earth_r0*(4/3)
# selection of reflection surface values and corresponding ce in km [N0n, cen]
# US average is N0=313
N0 = array([[200, 0.1184], [250, 0.1256], [301, 0.1396], [313, 0.1439], [400, 0.1867], [450, 0.2233]])
    