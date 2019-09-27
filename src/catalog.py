import pickle,json

from matplotlib import use
use("Agg")
import matplotlib.pyplot as plt

from Messier33.include.m33 import *
from Messier33.include.config import *
from Messier33.src.source import Source

class Catalog(object):
    def __init__(self, catalog="null", size=0):
        #self.sources=[Source]*size
        #self.sources=np.array([Source()]*size)#, dtype=Source)
        self.sources = [Source()]*size

        self.catalog=catalog

    @classmethod
    def from_pandas(cls, filename="%s/pandas_m33_2009.unique"%DATA):
        _size=cls.filelength(filename)
        cls=cls(catalog="pandas", size=_size)
        bandINFO_step=31
        with open(filename, 'r') as raw:
            for i,line in enumerate(raw.readlines()[:]):
                #_skycoord=cls.line_to_skycoord(line[:24].split())
                _skycoord=None
                _bandDATA=cls.line_to_bandINFO(line[24:55], band='g')
                _bandDATA.update(cls.line_to_bandINFO(line[55:86], band='i'))
                #cls.sources[i]=cls.sources[i](skycoord=_skycoord, bandDATA=_bandDATA)
                cls.sources[i]=Source(skycoord=_skycoord, bandDATA=_bandDATA)
                if(i%1000==0): print("%f"%(float(i)/_size)) 
        #cls.sources = np.array(cls.sources)
        return cls

    @classmethod
    def from_wfcam(cls, filename="%s/wfcam_m33_lot.unique"%DATA):
        _size=cls.filelength(filename)
        cls=cls(catalog="wfcam", size=_size)
        with open(filename, 'r') as raw:
            for i,line in enumerate(raw.readlines()[:]):
                _skycoord=cls.line_to_skycoord(line[:27].split())
                _bandDATA=cls.line_to_bandINFO(line[30:61], band='J')
                _bandDATA.update(cls.line_to_bandINFO(line[61:92], band='K'))
                _bandDATA.update(cls.line_to_bandINFO(line[92:123],band='H'))
                cls.sources[i]=Source(skycoord=_skycoord, bandDATA=_bandDATA)
        return cls


    @classmethod
    def from_serialised(cls, filename="%s/out/tmp.npy"%ROOT):
        with open(filename,'rb') as serial_in:
            #cls=json.load(serial_in, object_hook=dict_to_obj)
            #cls=pickle.load(serial_in)
            cls=np.load(filename, allow_pickle=True)
        return(cls)

    @staticmethod
    def line_to_skycoord(rawline): #this is very slow
        ra="%s:%s:%s"%(rawline[0], rawline[1], rawline[2])
        dec="%s:%s:%s"%(rawline[3], rawline[4], rawline[5])
        return(SkyCoord(ra=ra,dec=dec,unit="deg"))

    @staticmethod
    def line_to_bandINFO(rawline, band="?"):
        #print(rawline[14:21], rawline[21:28], rawline[28:])
        bandINFO={  globals()["%s"%band]:   float(rawline[14:21]),
                    globals()["d%s"%band]:  float(rawline[21:28]),
                    globals()["%scls"%band]:float(rawline[28:])}
        return(bandINFO)

    @staticmethod
    def filelength(filename):
        with open(filename) as f:
            for i,l in enumerate(f): pass
        return i+1
    
    def serialise(self):
        #temporary till i do filename
        filename="%s/out/tmp.npy"%ROOT
        with open(filename,'wb') as serial_out:
            #json.dump(self, serial_out, default=convert_to_dict)
            #pickle.dump(self,serial_out, protocol=0)#, default=convert_to_dict))
            np.save(filename, self)

    @property
    def g(self): #not ideal but ok for now
        return(s[g] for s in self.sources)
    @property
    def i(self): #not ideal but ok for now
        return(s[i] for s in self.sources)
    
if __name__=="__main__":
    import time
    #c=Catalog.from_pandas(filename="%s/pandas.test"%DATA)
    #c=Catalog.from_wfcam(filename="%s/wfcam.test"%DATA)
    c=Catalog.from_pandas(filename="%s/../initial/pandas_m33_2009.unique"%DATA)
    c.serialise()
    print("dumpes")
    c=Catalog.from_serialised()
    print(c.g)



