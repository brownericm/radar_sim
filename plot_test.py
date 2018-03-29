# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 21:44:59 2018

@author: brown
"""

import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0,2,100)
plt.plot(x,x,label='linear')
plt.plot(x,x**2, label='quadratic')
plt.plot(x,x**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()
plt.show()