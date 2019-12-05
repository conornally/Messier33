from Messier33.src.database import *


class Isochrone(DataBase):
    def __init__(self, data, params={}, indices={}, bands=[]):
        self.params=params
        super(Isochrone,self).__init__(data,indices=indices, bands=bands)

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

    def __repr__(self): return("[Fe/H]=%.2f t=%.1fGyr"%(self.params['feh'],self.params['age']))

    def lower_maglimit(self, value, key, inverse=True):
        """
        INPUT:  value=value below which will be removed
                key=key on which to crop
                inverse=True/False keep below/above value
        FUNC:   mostly useful for setting a lower magnitude limit.
                > cuts values above or below a given threshold
        """
        mask=Messier33.mask.Cut(key,value, inverse=inverse)
        self=mask.apply_on(self,True)


if(__name__=="__main__"):
    iso = Isochrone.from_dartmouth("tests/test.iso")
    print(iso)
    print(iso.indices)
    print(iso['g'][0], iso['g'][-1])
    iso.apply_distance_modulus(10,807e3)
    print(iso['g'][0], iso['g'][-1])
    iso.lower_maglimit('g',26)
    print(iso['g'][0], iso['g'][-1])
    print(len(iso))
    print(max(iso['g']),min(iso['g']))
