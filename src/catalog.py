import pickle,json

from matplotlib import use
use("Agg")
import matplotlib.pyplot as plt

from Messier33.include.m33 import *
from Messier33.include.config import *
from Messier33.src.loading import Loading
from Messier33.src.fileio import *


class Catalog(object):
    def __init__(self, data=[], size=(0,0), style="null", name="null", indices=[]):
        self._data = data
        self.style=style
        self.name=name
        self.size=size
        self.indices={}
        self.bands=[]
        for i,key in enumerate(indices):
            self.indices[key]=i
            if("cls" in key): self.bands.append(key[0])
            
    def colour(self, band1, band2):
        return( self[band1]-self[band2] )

    def crop(self, removing=(1,0,-9,-8.-3)):
        """
        INPUT:  removing = source classes to be removed from catalog
                -1  stellar
                -2  probably stellar
                -3  compact but non-stellar
                -8  poor match ie. not within 1 arcsec but within 2.5 arcsec
                -9  saturated
                 0  noise-like
                 1  non-stellar
        FUNC:   crops "removing" list out of catalog
        """
        mask = ([True]*len(self))
        for band in self.bands:
            for cls_crop in removing:
                mask*= (self["%scls"%band]!=cls_crop)
        self._data = self._data[mask]
        self.name+=".cropped"

    """
    def radial_distribution(self, origin=(0,0)):
        dist = [ s.getradius(origin) for s in self.sources ]
        return(dist)
    """

    def __len__(self):
        return(self._data.shape[0])

    def __getitem__(self, key):
        return( self._data[:,self.indices[key]])

    @classmethod
    def from_dict(cls, raw_dict):
        cls = cls(  data=raw_dict["data"],
                    style=raw_dict["style"],
                    size=raw_dict["size"], 
                    indices=raw_dict["indices"])
        return cls

    @classmethod
    def from_pandas(cls, filename):
        cls=cls.from_dict(import_from_raw(filename, style="pandas"))
        cls.name=filename.split('/')[-1]
        return cls
    
    @classmethod
    def from_wfcam(cls, filename):
        cls=cls.from_dict(import_from_raw(filename, style="wfcam"))
        cls.name=filename.split('/')[-1]
        return cls

    @classmethod
    def from_serialised(cls, filename):
        cls=cls.from_dict(import_from_serialised(filename))
        cls.name=filename.split('/')[-1]
        return cls

    def to_dict(self):
        return({"data":self._data,
                "style":self.style,
                "size":self.size,
                "indices":list(self.indices.keys())})

    def export(self, filename=''):
        if(filename==''): filename="%s/%s.pickle"%(OUT, self.name)
        serialise(filename, self.to_dict())


if __name__=="__main__":
    #c=Catalog.from_pandas(filename="%s/pandas.test"%DATA)
    #c=Catalog.from_pandas(filename="%s/../initial/pandas_m33_2009.unique"%DATA)
    #c=Catalog.from_pandas_to_array(filename="%s/pandas.test"%DATA)
    #c=Catalog.from_pandas_to_array(filename="%s/../initial/pandas_m33_2009.unique"%DATA)
    #c=Catalog.from_wfcam(filename="%s/wfcam.test"%DATA)
    #c.export()
    c=Catalog.from_serialised("%s/wfcam.test.pickle"%OUT)
    c.crop()

    #c.crop()
