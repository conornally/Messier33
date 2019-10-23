import numpy as np
import Messier33
from astropy.coordinates import SkyCoord
import astropy.units as u
from dustmaps.sfd import SFDQuery

class Catalog(object):
    def __init__(self, data=[], size=(0,0), style="null", name="null", indices={}, units="deg", history=[]):
        self._data = data
        self.style=style
        self.name=name
        self.size=size
        self.units=units
        self.indices = indices
        if(style=="pandas"): self.config=Messier33.pandas_config
        self.history=history

    def __len__(self):
        return(self._data.shape[0])

    def remove_nonstellar(self):
        Messier33.info("*Removing non-stellar sources from catalog\n")
        for band in self.bands:
            mask = Messier33.mask.Bool([-1,-2], "%scls"%band)
            self = mask.apply_on(self, overwrite=True)
        self.history.append("Removed any non-stellar sources from catalog")

    @property
    def bands(self):
        bands=[]
        for key in self.indices.keys(): 
            if("cls" in key): bands.append(key[0])
        return bands

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
    
    def append(self, data, key="key"):
        """
        INPUT:  list of values [1x(len(catalog))]
                key = indexing key if desired
        FUNC:   combines input list into Catalog._data
        """
        if(len(data)!=len(self)): raise ValueError("Input list must be of shape (1,%d), recieved %s"%(len(self), np.shape(data)))
        if(key in self.indices): raise KeyError("key='%s' exists in data set"%key)
        self._data = np.append( self._data, np.empty((len(self),1)), axis=1)
        self.indices[key] = len(self[0])-1
        self[key] = data
        self.history.append("Appended %s column in position %d"%(key,self.indices[key]))

    def replace(self, data, key, rename_key=""):
        """
        INPUT:  list of values as column
                key = key in catalog to replace
        """
        if(len(data)!=len(self)): raise ValueError("Input list must be of shape (1,%d), recieved %s"%(len(self), np.shape(data)))
        if(key not in self.indices): raise KeyError("key='%s' does not exist in data set"%key)
        self[key] = data
        if(rename_key): self.indices[rename_key] = self.indices.pop(key)
        self.history.append("Replaced %s column in position %d"%(key,self.indices[key]))

    def delete(self, key):
        """
        INPUT:  key=(str) of column to delete from data
                    (int) or (slice) of rows to delete
        FUNC:   removes portion of dataset
        """
        print(key, type(key))
        if(type(key)==str):
            if(key not in self.indices): raise KeyError("key='%s' does not exist in data set"%key)
            self._data=np.delete(self._data, self.indices[key], axis=1)
            self.indices.pop(key)
        else:
            self._data=np.delete(self._data, key, axis=0)
        self.history.append("Deleted %s from dataset"%key)


    @classmethod
    def copy(cls, other):
        other_dict=other.to_dict()
        cls = cls.from_dict(other_dict)
        return(cls)

    @classmethod
    def from_dict(cls, raw_dict):
        cls = cls(  data=raw_dict["data"],
                    style=raw_dict["style"],
                    size=raw_dict["size"], 
                    indices=raw_dict["indices"], 
                    units=raw_dict["units"],
                    history=raw_dict["history"])
        return cls

    @classmethod
    def from_pandas(cls, filename):
        cls=cls.from_dict(Messier33.io.import_from_raw(filename, style="pandas"))
        cls.name=filename.split('/')[-1]
        return cls
    
    @classmethod
    def from_wfcam(cls, filename):
        cls=cls.from_dict(Messier33.io.import_from_raw(filename, style="wfcam"))
        cls.name=filename.split('/')[-1]
        return cls

    @classmethod
    def from_serialised(cls, filename):
        cls=cls.from_dict(Messier33.io.import_from_serialised(filename))
        cls.name=filename.split('/')[-1]
        return cls

    def mean(self, key='g'):
        if(key not in self.indices): raise KeyError("key='%s' not in data set"%key)
        return(np.mean(self[key]))

    def to_dict(self):
        return({"data":self._data,
                "style":self.style,
                "size":self.size,
                "indices":self.indices,
                "units":self.units,
                "history":self.history})

    def export(self, filename=''):
        if(filename==''): filename="%s/%s.pickle"%(Messier33.OUT, self.name)
        Messier33.io.serialise(filename, self.to_dict())

    def convert_to_stdcoords(self, A=0, D=0):
        Messier33.info("*Converting RADEC to Standard Coordinates\n")
        if(not A):A=Messier33.ra
        if(not D):D=Messier33.dec
        if(self.units=="deg"):
            self['ra'] = np.radians(self['ra'])
            self['dec'] = np.radians(self['dec'])
            self.units="rads"
        if(self.units=="rads"):
            #for now this overwrites the ra/dec column, can change this if needed
            xi = (np.cos(self['dec'])*np.sin(self['ra']-A))/( np.sin(D)*np.sin(self['dec'])+np.cos(D)*np.cos(self['dec'])*np.cos(self['ra']-A))
            eta= (np.cos(D)*np.sin(self['dec'])-np.sin(D)*np.cos(self['dec'])*np.cos(self['ra']-A))/(np.sin(D)*np.sin(self['dec'])+np.cos(D)*np.cos(self['dec'])*np.cos(self['ra']-A))
            self.units="stdcoord"
            self.append(np.degrees(xi), "xi")
            self.append(np.degrees(eta), "eta")
        self.history.append("Converted RADEC to STDCoordinates")

    def deproject_radii(self):
        #not sure best interface, should i add to _data, or create a new thing, or just return it
        #Cioni09.3 - 2.3
        Messier33.info("*Deprojecting radii\n")
        Q = Messier33.PA - np.radians(90)
        _x = self['xi']*np.cos(Q) + self['eta']*np.sin(Q)
        _y = -self['xi']*np.sin(Q) + self['eta']*np.cos(Q)
        _y /= Messier33.inclination
        self.append(np.sqrt( _x**2.0 + _y**2.0) ,key="dist")
        self.history.append("Deprojected Radii from galactic centre")
        return(self['dist'])

    def correct_dust(self, overwrite=True):
        """
        INPUT:  overwrite (True) filter mag column with corrected magnitudes
        FUNC:   using SFDQuery finds E(B-V) for each ra,dec in catalog and 
                corrects the filter magnitudes using this value
        """
        Messier33.info("*Correcting Dust Extinction\n")
        if(self.style=="wfcam"): raise NotImplementedError("wfcam dust correction not implenemted yet")
        coords = SkyCoord(self['ra'], self['dec'], unit=u.deg)
        ebv = SFDQuery()(coords)
        
        go = self['g'] - (self.config.g_dust_coeff*ebv)
        io = self['i'] - (self.config.i_dust_coeff*ebv)
        if(overwrite):
            self.replace(go, "g")
            self.replace(io, "i")
            self.indices["go"]=self.indices["g"]
            self.indices["io"]=self.indices["i"]
        else:
            self.append(go, "go")
            self.append(io, "io")
        self.history.append("Extinction Correction in bands g,i")

    def apply_distance_modulus(self, d1, d2=10, overwrite=True):
        """
        INPUT:  d1=current distance of sources [pc]
                d2=new distance of sources (default to 10pc
                #might just make this always true #overwrite (True) overwrites each magnitude band
        FUNC:   scales apparent magnitudes to appear as though they were at d2
                m2 = m1 - 5log10(d1/d2)
        """
        Messier33.info("Scaling distance from %f --> %f\n"%(d1,d2))
        dist_modulus = 5*np.log10(d1/d2)
        for band in self.bands:
            if(overwrite): self.replace(self[band]-dist_modulus, band)
            else: self.append(self[band]-dist_modulus)
        self.history.append("Moved galactic distance from %f to %f updating magnitudes accordingly"%(d1,d2))

if __name__=="__main__":
    c=Catalog.from_pandas(filename="%s/test/pandas.test"%Messier33.DATA)
    #c=Catalog.from_pandas(filename="%s/initial/pandas_m33_2009.unique"%Messier33.DATA)
    #c=Catalog.from_pandas_to_array(filename="%s/pandas.test"%Messier33.DATA)
    #c=Catalog.from_pandas_to_array(filename="%s/../initial/pandas_m33_2009.unique"%Messier33.DATA)
    #c=Catalog.from_wfcam(filename="%s/wfcam.test"%Messier33.DATA)
    #c.export()
    #c=Catalog.from_serialised("%s/wfcam.test.pickle"%Messier33.OUT)
    #c.crop()
    #c.convert_to_stdcoords()
    #c.deproject_radii()
    #c.correct_dust(overwrite=False)
