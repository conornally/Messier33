import Messier33

class Isochrone(object):
    def __init__(self, data, params={}, indices={}):
        self._data=data
        self.params=params
        self.indices=indices

    @classmethod
    def from_dartmouth(cls, filename):
        raw_dict=Messier33.io.from_dartmouthISO(filename)
        return cls.from_dict(raw_dict)

    @classmethod
    def from_dict(cls, raw_dict):
        return(cls(raw_dict["data"],
                    params=raw_dict["params"],
                    indices=raw_dict["indices"]))

    def __getitem__(self, key):
        if(type(key)==int or type(key)==slice): return self._data[key]
        elif(type(key)==tuple or type(key)==list): return(np.array([self[col] for col in key]))
        elif('-' in key): #for doing colours
            a,b = key.split('-')
            return(self[a]-self[b])
        else: 
            if(key not in self.indices): raise KeyError("key=%s not in indices"%key)
            return( self._data[:,self.indices[key]])

    def __repr__(self): return("%s"%self.params)

if(__name__=="__main__"):
    iso = Isochrone.from_dartmouth("/home/conor/data/m33/isochrones/notes/data/test.iso")
    print(iso)
    print(iso.indices)
    print(iso['g'][0])

