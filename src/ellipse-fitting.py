import sys
import numpy as np
from astropy.io import fits

from photutils import isophote

# load fits
# load config
# get isolist
# convert pixels to degrees (or arcmin)
# return intensity vs degrees

def load_config(filename):
    rawdict={'x':0, 'y':0, 'PA':0, 'sm0':0, 'sm1':2000, 'sma':400, 'geosma':500, 'e':0}
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            _line=line.split()
            rawdict[_line[0]] = float(_line[1])
    return(rawdict)


def getIsoList(data, config):
    geometry=isophote.EllipseGeometry(config['x'], config['y'], 
                                      config['geosma'], config['e'], 
                                      np.radians(config['PA']))
    print(geometry.__dict__)
    ellipse=isophote.Ellipse(data, geometry, threshold=0.01)
    return(ellipse.fit_image(config['sma'], config['sm0'], config['sm1']))

if(__name__=="__main__"):
    config=load_config("/mnt/sd/data/m33/ellipse/conf")
    data=fits.open("/mnt/sd/data/m33/ellipse/m33_i_mosaic.fits")[0].data
    print(getIsoList(data,config).sma)


