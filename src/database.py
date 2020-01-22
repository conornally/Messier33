import numpy as np
import Messier33

class DataBase(object):
    """
    Parent class for astronomical data analysis
    Porbably not designed to run on its own, like you could but itd be pretty boring
    Initialise with data array and indices dictionary of names and columns

    This class is mostly bare bones file and catalog manipultions
    > with some useful astroy functions thrown in
    """
    def __init__(self, data, indices={}, history=[], name="null", bands=[]):
        self.name=name
        self.data=data
        self.indices=indices
        self.history=history
        self.bands=bands

    def __getitem__(self, key):
        if(type(key)==int or type(key)==slice): return self.data[key]
        elif(type(key)==tuple or type(key)==list): return(np.array([self[col] for col in key]))
        elif('-' in key): #for doing colours
            a,b = key.split('-')
            return(self[a]-self[b])
        else: 
            if(key not in self.indices): raise KeyError("key=%s not in indices"%key)
            return( self.data[:,self.indices[key]])
    
    def __setitem__(self, key, item):
        if(type(key)==int): self.data[key]=item
        else: self.data[:,self.indices[key]]=item

    def __len__(self): return(self.data.shape[0])
    def __repr__(self): return("%s"%self.name)

    def add_index(self, key, value, overwrite=True):
        """
        INPUT:  key -  new index key 
                value- new index value
                overwrite - if True (default) will overwrite existing key
        """
        if(key in self.indices.keys() and not overwrite): raise KeyError("%s in indices already, set 'overwrite=True' to overwrite it")
        Messier33.debug("Adding new index %s=%d\n"%(key,value))
        self.indices[key]=int(value)
        self.history.append("03-New index %s=%d"%(key,value))



    def append(self, data, key="key"):
        """
        INPUT:  list of values [1x(len(catalog))]
                key = indexing key if desired
        FUNC:   combines input list into Catalog.data
        """
        if(len(data)!=len(self)): raise ValueError("Input list must be of shape (1,%d), recieved %s"%(len(self), np.shape(data)))
        if(key in self.indices): raise KeyError("key='%s' exists in data set"%key)
        self.data = np.append( self.data, np.empty((len(self),1)), axis=1) #why did i do it this way again
        self.indices[key] = len(self[0])-1
        self[key] = data
        self.history.append("00-Appended %s column in position %d"%(key,self.indices[key]))

    def replace(self, data, key, rename_key=""):
        """
        INPUT:  list of values as column
                key = key in catalog to replace
        """
        if(len(data)!=len(self)): raise ValueError("Input list must be of shape (1,%d), recieved %s"%(len(self), np.shape(data)))
        if(key not in self.indices): raise KeyError("key='%s' does not exist in data set"%key)
        self[key] = data
        if(rename_key): self.indices[rename_key] = self.indices.pop(key)
        try:self.history.append("01-Replaced %s column in position %d"%(key,self.indices[key]))
        except:self.history.append("01-Replaced %s column in position %d"%(key,self.indices[rename_key]))

    def delete(self, key):
        """
        INPUT:  key=(str) of column to delete from data
                    (int) or (slice) of rows to delete
        FUNC:   removes portion of dataset
        """
        if(type(key)==str):
            if(key not in self.indices): raise KeyError("key='%s' does not exist in data set"%key)
            self.data=np.delete(self.data, self.indices[key], axis=1)
            self.indices.pop(key)
            #URGENT UPDATE FOLLOWING INDICES
        else:
            self.data=np.delete(self.data, key, axis=0)
        self.history.append("02-Deleted %s from dataset"%key)

    def to_dict(self): return(self.__dict__)

    @classmethod
    def from_serialised(cls, filename):
        cls=cls.from_dict(Messier33.io.import_from_serialised(filename))
        cls.name=filename.split('/')[-1]
        return cls

    @classmethod
    def from_dict(cls, raw_dict):
        return(cls(raw_dict["data"], indices=raw_dict["indices"],
                    history=raw_dict["history"], name=raw_dict["name"],
                    bands=raw_dict["bands"]))

    @classmethod
    def copy(cls, other):
        other_dict=other.to_dict()
        print(type(cls))
        print(other_dict["shell_areas"])
        cls = cls.from_dict(other_dict)
        return(cls)

    def export(self, filename=''):
        if(filename==''): filename="%s/%s.pickle"%(Messier33.OUT, self.name)
        Messier33.io.serialise(filename, self.to_dict())

    def export_ascii(self, filename=''):
        if(filename==''):filename="%s/%s.tab"%(Messier33.OUT, self.name)
        Messier33.info("*Exporting to %s\n"%filename)
        _head = sorted(self.indices.items(), key=lambda x:x[1])
        head=''
        for x in _head: head+="%s "%x[0]
        np.savetxt(filename, self.data, header=head)

    ######
    #here the cooler moreuseful astro functions reside
    ####

    def apply_distance_modulus(self, d1, d2=10):
        """
        INPUT:  d1=current distance of sources [pc]
                d2=new distance of sources (default to 10pc
                #might just make this always true #overwrite (True) overwrites each magnitude band
        FUNC:   scales apparent magnitudes to appear as though they were at d2
                m2 = m1 - 5log10(d1/d2)
        """
        Messier33.info("Scaling distance from %f --> %f\n"%(d1,d2))
        dist_modulus = 5*np.log10(d1/d2)
        print(dist_modulus)
        for band in self.bands:
            self.replace(self[band]-dist_modulus, band)
            if("%so"%band in self.indices): self.replace(self["%so"%band]-dist_modulus, "%so"%band)
        self.history.append("Moved galactic distance from %f to %f updating magnitudes by %f"%(d1,d2, dist_modulus))

if(__name__=="__main__"):
    db=DataBase(np.zeros((5,2)), indices={'x':0,'y':1})
    db2=DataBase.copy(db)
    print(db2['x'])
