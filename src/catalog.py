
from Messier33.include.m33 import *
from Messier33.include.config import *
from Messier33.src.source import Source

class Catalog(object):
    def __init__(self, catalog="null", size=0):
        self.sources=[Source]*size
        #self.sources=np.array([Source]*size, dtype=Source)
        self.catalog=catalog

    @classmethod
    #def from_pandas(cls, filename="%s/pandas_m33_2009.unique"%DATA):
    def from_pandas(cls, filename="%s/pandas.test"%DATA):
        _size=cls.filelength(filename)
        cls=cls(catalog="pandas", size=_size)
        with open(filename, 'r') as raw:
            for i,line in enumerate(raw.readlines()[:]):
                line=line.split()
                _skycoord=cls.line_to_skycoord(line[:6])
                _bandDATA=cls.line_to_bandINFO(line[6:11], band='g')
                _bandDATA.update(cls.line_to_bandINFO(line[11:16], band='i'))
                cls.sources[i]=cls.sources[i](skycoord=_skycoord, bandDATA=_bandDATA)
        return cls

    @staticmethod
    def line_to_skycoord(rawline):
        ra="%s:%s:%s"%(rawline[0], rawline[1], rawline[2])
        dec="%s:%s:%s"%(rawline[3], rawline[4], rawline[5])
        return(SkyCoord(ra=ra,dec=dec,unit="deg"))

    @staticmethod
    def line_to_bandINFO(rawline, band="?"):
        bandINFO={  "%sx"%band:float(rawline[0]),
                    "%sy"%band:float(rawline[1]),
                    band:float(rawline[2]),
                    "%serr"%band:float(rawline[3]),
                    "%scls"%band:float(rawline[4])}
        return(bandINFO)

    @staticmethod
    def filelength(filename):
        with open(filename) as f:
            for i,l in enumerate(f): pass
        return i+1


if __name__=="__main__":
    c = Catalog().from_pandas()
    print(c.sources[0:2]['g'])



