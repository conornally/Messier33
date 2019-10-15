import numpy as np
#https://ned.ipac.caltech.edu/byname?objname=m33&hconst=67.8&omegam=0.308&omegav=0.692&wmap=4&corr_z=1
ra = np.radians(23.462042)
dec= np.radians(30.660222)
PA = np.radians(-35) ##tmp
inclination = np.radians(53) 
a = 7.50E-02 ##dont really get this number
b = 7.50E-02

def hms_to_degrees(h,m,s):
    return((h*15.0)+(m/4.0)+(s/240.0))

def dms_to_degrees(d,m,s):
    return(d+(m/60.0)+(s/3600.0))

