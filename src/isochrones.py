from Messier33.src.database import *


class Isochrone(DataBase):
    def __init__(self, data, params={}, indices={}, bands=[]):
        self.params=params
        super(Isochrone,self).__init__(data,indices=indices, bands=bands)

    @classmethod
    def from_dartmouth(cls, filename, colours="PanSTARRS"):
        if(colours=="PanSTARRS"): raw_dict=Messier33.io.ISOfrom_Dartmouth_PanSTARRS(filename)
        return cls.from_dict(raw_dict)

    @classmethod
    def from_padova(cls, filename, colours="PanSTARRS"):
        if(colours=="PanSTARRS"): raw_dict=Messier33.io.ISOfrom_PadovaPanSTARRS(filename)
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

    ##########
    # BODGES #
    ##########

    def pseudo_dustcorrect(self):
        """
        FUNC:   isochrones come dust corrected, this adds an index with 'o' suffix to each band
        """
        for band in self.bands:
            self.add_index("%so"%band, self.indices[band])

if(__name__=="__main__"):
    iso = Isochrone.from_padova("/home/conor/Downloads/output402857142341.dat", "PanSTARRS")
    print(iso)
    print(iso.indices)
    iso.pseudo_dustcorrect()
    print(iso.indices)
    iso.export("%s/test-iso.pickle"%Messier33.OUT)
    iso=Isochrone.from_serialised("%s/test-iso.pickle"%Messier33.OUT)
    print(iso)
    print(iso.indices)
