import numpy as np
import Messier33

class Isochrone(object):
    def __init__(self, data, params={}, indices={}, bands=[]):
        self._data=data
        self.params=params
        self.indices=indices
        self.bands=bands

    @classmethod
    def from_dartmouth(cls, filename):
        raw_dict=Messier33.io.from_dartmouthISO(filename)
        return cls.from_dict(raw_dict)

    @classmethod
    def from_dict(cls, raw_dict):
        return(cls(raw_dict["data"],
                    params=raw_dict["params"],
                    indices=raw_dict["indices"],
                    bands=raw_dict["bands"]))

    def __getitem__(self, key):
        if(type(key)==int or type(key)==slice): return self._data[key]
        elif(type(key)==tuple or type(key)==list): return(np.array([self[col] for col in key]))
        elif('-' in key): #for doing colours
            a,b = key.split('-')
            return(self[a]-self[b])
        else: 
            if(key not in self.indices): raise KeyError("key=%s not in indices"%key)
            return( self._data[:,self.indices[key]])

    def __setitem__(self, key, item):
        if(type(key)==int): self._data[key]=item
        else: self._data[:,self.indices[key]]=item

    def apply_distance_modulus(self, d1, d2=10): 
        """
        INPUT:  d1=current distance of sources [pc]
                d2=new distance of sources (default to 10pc)
        FUNC:   scales apparent magnitudes to appear as though they were at d2
                m2 = m1 - 5log10(d1/d2)
        """
        Messier33.info("Scaling distance from %f --> %f\n"%(d1,d2))
        dist_modulus = 5*np.log10(d1/d2)
        for band in self.bands:
            self[band]-=dist_modulus

    def __repr__(self): return("[Fe/H]=%.2f t=%.1f"%(self.params['feh'],self.params['age']))

if(__name__=="__main__"):
    iso = Isochrone.from_dartmouth("/home/conor/data/m33/isochrones/notes/data/test.iso")
    print(iso)
    print(iso.indices)
    print(iso['g'][-1])
    iso.apply_distance_modulus(10,807e3)
    print(iso['g'][-1])

