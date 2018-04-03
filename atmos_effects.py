# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:03:38 2018

@author: brown
@ref: Mahafza
@ref: AESS IEEE NH Section, Radar Graduate Course

Technically this is atmos and ground effects
"""
from radarparams import range_max, freq, pt
from envconst import wvd, c0, kb, r0, re
from convert import deg2rad, rad2deg, km2m
from scipy.special import i0
from scipy import interpolate, sqrt
from numpy import angle, linspace, append, arcsin, arccos, cos, exp, sin, pi
import numpy as np


def s_rough_e(hrms, psig):
    """
    Calculate surface roughness according to exponential representation of surface roughtness
    Inputs:
        hrms = average roughness of surface RMS (root mean squared) value
    Outputs:
        sr = Surface Roughness
    """
    #exponential representation of surface roughtness
    lambda_ = c0/freq
    inner = (2 * pi * hrms * sin(psig)/lambda_)**2
    sr = exp(-2*inner)
    return sr

def s_rough_b(hrms, psig):
    """
    Calculates surface roughness with zeroth order bessel (Supposedly more accurate)
    Inputs:
        hrms = average roughness of surface RMS (root mean squared) value
    Outputs:
        sr = Surface Roughness
    """
    lambda_ = c0/freq
    z = 2*((2*pi*hrms*sin(psig))/lambda_)
    sr = exp(-z)*i0(z)
    return sr

def divergence(psig, r1, r2, hr, ht):
    """
    Inputs:
        psig = grazing angle in radians
        r1 = ground range to bounce point in meters
        r2 = ground range to bounce point on target sidde in meters
        hr = hieght radar in meters
        ht = height target in meters
    Outputs:
        div = divergence value
    #This will need a toggle for different earth models sphere or 4/3
    # 4/3 case
    """
    re_m = km2m(re)
    r = r1 + r2
    num = (re_m*r*sin(psig)*cos(psig))
    denom = ((2*r1*r2/cos(psig))+re_m*r*sin(psig))*(1+hr/re_m)*(1+ht/re_m)
    div = sqrt(num/denom)

    return div

def refl_coef(psig, eps_p, eps_pp):
    """
    Inputs:
        psig = grazing angle (incident angle)
        eps_p = real part of dielectric const
        eps_pp = imag part of dielectric const
    Outputs:
        Gamma_v = vertically polarized refl coeff
        Gamma_h = horiz polarized refl coeff

    TODO: Implement full lookup table for eps_p and eps_pp
    TODO: Add LHCP and RHCP cases
    TODO: Add Sea State lookup
    """
    eps = eps_p - 1j*eps_pp
    arg1 = eps - (cos(psig)**2)
    arg2 = sqrt(arg1)
    arg3 = sin(psig)
    arg4 = eps*arg3
    rv = (arg4-arg2)/(arg4+arg2)
    rh = (arg3-arg2)/(arg3+arg2)
    #Gamma_v = (eps * sin(psig)-sqrt(eps-(cos(psig))**2))/(eps*sin(psig)+sqrt(eps-(cos(psig))**2))
    #Gamma_h = (sin(psig)-sqrt(eps-(cos(psig))**2))/(sin(psig)+sqrt(eps-(cos(psig))**2))

    return rv, rh

def atmo_absorp(ht, hr, freq, beta):
    """
    Inputs:
        ht = height of target in Km
        wvd = water vapor density g/m^3
        freq = radar operating frequency in GHz
        beta = radar wave path elev. angle in deg
    Outputs:
        gammaO2 = atmospheric attenuation due to O2 dB
        gammaH2O = atmospheric attenuaation due to H2O dB
        range_vec = range array with corralary dimensions to gamma

    Note: This is straight from Mahafza and the numbers are obfuscated by weird
    programming decisions.

    I spent way too much time figuring out how to interpolate wvd from book into
    an arbitrary height lookup

    !!! for now target must be above radar

    TODO: Revise to make clearer
    TODO: Think about the best way to construct height vector
    TODO: Clean up booleans, I used bitwise instead of logical booleans which is why it is so messy
    ---
    DONE: Implement Lookup or function for wvd at alt
    """

    v1 = 0.018 # "v_n" values from chapter 8 references "Van Vleek"
    #v2 = 0.05
    #v3 = .1
    #v4 = 0.3
    #ht = ht * 1000 # convert to meters for arange() consistancy
    #hr = hr * 1000
    h_vec = linspace(hr, ht, 999) # Make linspace() or arange() array of heights so we can integrate over an array of ranges?

    near = abs(h_vec - wvd[4,0]).argmin()

    if (ht < wvd[4,0]) | (hr < wvd[4,0]):
        fn = interpolate.interp1d(wvd[0:5,0],wvd[0:5,1], kind = 'cubic')
        wvd_low = fn(h_vec[:near])
        if (ht < wvd[4,0]) & (hr < wvd[4,0]):
            wvd_long = wvd_low

    if (ht > wvd[4,0]) | (hr > wvd[4,0]):
        fn2 = interpolate.interp1d(wvd[4:,0],wvd[4:,1])
        wvd_high = fn2(h_vec[near+1:])
        if (ht > wvd[4,0]) & (hr > wvd[4,0]):
            wvd_long = wvd_high

    if ((ht < wvd[4,0]) | (hr < wvd[4,0])) & ((ht > wvd[4,0]) | (hr > wvd[4,0])):
        wvd_long = append(wvd_low,wvd_high)
        wvd_long = append(wvd_long, wvd_long[-1])

    lambda_cm = 3E10/(freq*10**9)
    T = 288 - 6.7*h_vec
    pressure = 1015 * (1-0.02275*h_vec)**(5.2561)
    P = (v1 * 0.4909 * pressure**2)/(T**(5/2))
    Q = v1**2 * 2.904E-4 * pressure **2 /T
    gammaO2 = P * (1/(1+Q*lambda_cm**2))*(1+ (1.39/lambda_cm**2))

    P = 1.852 * 3.165E-6 * wvd_long * pressure**2 / T**(3/2)
    Q1 = (1-0.742 * lambda_cm)**2
    Q2 = (1+0.742*lambda_cm)**2
    Q = 2.853E-6*pressure**2/T
    gammaH2O = P*((1/(Q1+Q*lambda_cm**2))+(1/(Q2+Q*lambda_cm**2))+3.43/lambda_cm**2)

    beta = deg2rad(beta)
    ec_hr = r0+hr # earth center heights for geometry reasons
    ec_ht = r0+h_vec
    alpha = arcsin(cos(beta)*ec_hr/ec_ht)
    theta = (pi/2)-beta-alpha
    range_vec = np.sqrt(ec_hr**2 + ec_ht**2 - 2*np.cos(theta)*ec_hr*ec_ht)
    #range_vec = ec_ht*np.sin(theta)/np.cos(beta)
    return gammaO2, gammaH2O, range_vec

def multipath(range_sl, ht, hr):
    """
    From Mahafza "Radar Systems Analysis and Design" pgs 300-303
    ht = height of target in meters
    hr = height of radar in meters
    range_sl = slant range to target (direct los range)

    Using the 4/3 earth model, we calculate the multipath range by determining the land range between target and radar and
    calculating the earth center angle between them. "re" is used as earther radius
    """
    check_range = sqrt(2*re)*(sqrt(ht)+sqrt(hr))
    if check_range > range_max:
       print("Range is beyond radar LOS")
       return
# ==========================
# Geometry
# ==========================
    Rd = range_sl

    #cast constants to meters
    # r0 = km2m(r0)
    re_m = km2m(re)
    val1 = Rd**2 - (ht -hr)**2
    val2 = 4 * (re_m + hr) * (re_m + ht)
    r = 2 * re_m * arcsin(sqrt(val1/val2))
    #r_num = (re_m+hr)**2+(re_m+ht)**2-Rd**2
    #r_denum = 2*(re_m+hr)*(re_m+hr)
    #r = re_m*arccos(np.sqrt(r_num/r_denum))
    p = (2/sqrt(3)) * sqrt(re_m * (ht + hr) + r**2 / 4) #Eq 8.94
    sai = arcsin((2 * re_m * r * (ht - hr))/p**3) #Eq 8.95
    r1 = r/2 - p*sin(sai/3) # Eq 8.93
    r2 = r - r1

    #phi = r / re_m # Eq 8.97
    phi1 = r1 / re_m # angle w/ vertex at center of earth with endpoints of bounce point and radar position
    phi2 = r2 / re_m

    R1 = sqrt(hr**2 + 4*re_m*(re_m + hr)*(sin(phi1/2))**2)
    R2 = sqrt(ht**2 + 4*re_m*(re_m + ht)*(sin(phi2/2))**2)
    psig = arcsin((2*re_m*hr + hr**2 - R1**2)/(2*re_m*R1)) #radian
    deltaR = R1 + R2 - Rd
    #deltaR = (4*R1*R2*(np.sin(psi)))**2/(R1+R2+Rd) #path difference

# ==========================
# Ground and Atmos Effects
# ==========================

    hrms = 1; #surface height irregularity
    lambda_ = c0/freq
    sr = s_rough_e(hrms, psig)
    #sr=1
    div = divergence(psig, r1, r2, hr, ht)
    #div=1
    eps_p = 50 # approx sea water @ 10Ghz
    eps_pp = 15
    Gamma_v, Gamma_h = refl_coef(psig, eps_p, eps_pp)
    #Gamma_v = 1
    #phi_h = angle(Gamma_h)
    phi_v = angle(Gamma_v)
    #phi_v = pi
    # Here I assume vertically polarized beam as it is more performant
    rho = abs(Gamma_v) * div * sr
    delta_phi = 2 * pi * deltaR / lambda_

    alpha = delta_phi + phi_v

    F = np.sqrt(1 + rho**2 + 2 * rho * cos(alpha)) # Propogation Factor Eq. 8.74
    return F
# =============================================================================
# def refraction(range_, el, N0_index, rho_max, hmax, freq):
#     """
#     Inputs:
#         range_ = actual range from Tx to target
#         el = elevation angle in deg
#         N0_index = N0 index (0-6) from the envconstants file
#         rho_max =
#     # In final version freq and range_ will be vector for PRFs, and will compute a vector output of
#     # all target refractions
#     """
#
#     return range_a, range_t, range_e
# =============================================================================
