import numpy as np
import Messier33

class Isochrone(object):
    def __init__(self):
        pass

    @classmethod
    def from_padova(cls, filename):
        size=Messier33.io.filelength(filename)
        load=Messier33.Loading(size,prefix=filename)
        with open(filename,'r') as infile:
            for i,line in enumerate(infile.readlines()):
                load(i)
                if(i==11): 
                    indices=Messier33.io.enum(line.strip("\n").split(' '))
                    _data=np.zeros((size,len(cls.extract_bands(indices))))
                 
        return cls

    @staticmethod
    def extract_bands(enum):
        index=[]
        for key,value in enum.items():
            if("mag" in key): index.append(value)
        return(index)

if(__name__=="__main__"):
    iso = Isochrone.from_padova("%s/data/isochrones/test.dat"%Messier33.ROOT)

