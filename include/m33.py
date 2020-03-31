import numpy as np
#https://ned.ipac.caltech.edu/byname?objname=m33&hconst=67.8&omegam=0.308&omegav=0.692&wmap=4&corr_z=1
ra = np.radians(23.462042)
dec= np.radians(30.660222)
PA = np.radians(-23) ## McConachie chapman etc 10 (Stellar halo and outer disc of m33
inclination = np.radians(53) 
inclination = np.radians(56) 
distance=809e+3
a = 7.50E-02 ##dont really get this number
b = 7.50E-02

def hms_to_degrees(h,m,s):
    return((h*15.0)+(m/4.0)+(s/240.0))

def dms_to_degrees(d,m,s):
    return(d+(m/60.0)+(s/3600.0))

def distance_modulus(d1,d2=10):
    return 5.0*np.log10(d1/d2)

def getName(catalog):
    names={ "full.pickle":"Full Catalogue",
            "rgb23.5.pickle":"RGB Shallow Cut",
            "rgb24.pickle":"RGB Deep Cut",
            "rsg.pickle":"RSG",
            "yms.pickle":"Young MS + BHeB",
            "agb.pickle":"AGB"}
    if(catalog.name in names.keys()): return names[catalog.name]
    else: return catalog.name.strip(".pickle")

def getColour(catalog):
    colours={   "full.pickle":'k',
                "rgb24.pickle":'r',
                "rgb23.5.pickle":'orange',
                "agb.pickle":"green",
                "yms.pickle":"purple",
                "rsg.pickle":"blue"}
    if(catalog.name in colours.keys()): return colours[catalog.name]
    else: return "grey"
            

def loadBackground(catalog):
    #this is getting horribly ungeneralised
    name=catalog.name[:catalog.name.index(".pickle")]
    bkg=np.genfromtxt("/home/conor/data/m33/structure.test/%s/%s.bkg"%(name, name))
    return bkg

def loadConf(catalog):
    name=catalog.name[:catalog.name.index(".pickle")]
    conf={}
    with open("/home/conor/data/m33/structure.test/%s/%s.conf"%(name,name), 'r') as fp:
        for line in fp.readlines():
            try:
                key,val = line.split('=')
                conf[key]=float(val)
            except:pass
    return(conf)

