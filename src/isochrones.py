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

    def __repr__(self): return("[Fe/H]=%.2f t=%.1f"%(self.params['feh'],self.params['age']))

if(__name__=="__main__"):
    iso = Isochrone.from_dartmouth("/home/conor/data/m33/isochrones/notes/data/test.iso")
    print(iso)
    print(iso.indices)
    print(iso['g'][-1])
    #iso.apply_distance_modulus(10,807e3)
    print(iso['g'][-1])

