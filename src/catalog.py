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
        self.sources_array=None

        self.catalog=catalog
        self.size=size

    @classmethod
    def from_pandas(cls, filename="%s/pandas_m33_2009.unique"%DATA):
        _size=cls.filelength(filename)
        cls=cls(catalog="pandas", size=_size)
        bandINFO_step=31
        with open(filename, 'r') as raw:
            for i,line in enumerate(raw.readlines()[:]):
                _skycoord=cls.line_to_skycoord(line[:24].split())
                #_skycoord=None
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
    def from_pandas_to_array(cls, filename="%s/pandas_m33_2009.unique"%DATA):
        _size=cls.filelength(filename)
        cls=cls(catalog="pandas", size=_size)
        cls.sources_array=np.zeros((_size,18))
        with open(filename, 'r') as file_in:
            for i,line in enumerate(file_in.readlines()):
                cls.sources_array[i] = cls.split_pandas_line(line)#, dtype=float)) #float automatic
        return cls

    @staticmethod
    def split_pandas_line(line, dtype=str):
        splitlist =[line[:3], line[3:6], line[6:12], 
                    line[12:16], line[16:19], line[19:24], 
                    line[24:31], line[31:38], line[38:45], line[45:52], line[52:55], 
                    line[55:62], line[62:69], line[69:76], line[76:83], line[83:86], 
                    line[86:89], line[89:93]]
        return(list(dtype(x) for x in splitlist))

    @classmethod
    def xfrom_serialised(cls, filename="%s/out/tmp.npy"%ROOT):
        with open(filename,'rb') as serial_in:
            #cls=json.load(serial_in, object_hook=dict_to_obj)
            #cls=pickle.load(serial_in)
            cls=np.load(filename, allow_pickle=True)
        return(cls)

    @staticmethod
    def line_to_skycoord(rawline): #this is very slow and SUPER memory intensive, i think ill convert to just float(degrees)
        ra="%s:%s:%s"%(rawline[0], rawline[1], rawline[2])
        dec="%s:%s:%s"%(rawline[3], rawline[4], rawline[5])
        return(SkyCoord(ra=ra,dec=dec,unit="deg"))

    @staticmethod
    def line_to_bandINFO(rawline, band="?"):
        bandINFO={  globals()["%s"%band]:   float(rawline[14:21]),
                    globals()["d%s"%band]:  float(rawline[21:28]),
                    globals()["%scls"%band]:float(rawline[28:])}
        return(bandINFO)

    @staticmethod
    def filelength(filename):
        with open(filename) as f:
            for i,l in enumerate(f): pass
        return i+1
    
    def xserialise(self):
        #temporary till i do filename
        filename="%s/out/tmp.npy"%ROOT
        with open(filename,'wb') as serial_out:
            #json.dump(self, serial_out, default=convert_to_dict)
            #pickle.dump(self,serial_out, protocol=0)#, default=convert_to_dict))
            np.save(filename, self)

    def serialise(self):
        with open("%s/tmp.serial"%OUT, "wb") as serial_out:

            sources = self.__dict__.pop("sources")
            serial_out.write(pickle.dumps(self.__dict__))
            serial_out.write(b"\nHEADER_END\n")
            for i,s in enumerate(sources):
                serial_out.write(s.serial)
                serial_out.write(b"\nDELIMETER\n")
                if(i%1000==0):print(i)
            serial_out.write(b"END\n")

    @classmethod
    def from_serialised(cls): #ok i think this sucks too, its just a memory problem
        with open("%s/tmp.serial"%OUT, "rb") as serial_in:
            stream=b""
            line=b""
            while(line!=b"HEADER_END\n"):
            #   for i in range(3):
                stream+=line
                line=serial_in.readline()
            cls=cls.from_dict(pickle.loads(stream))
            
            flag=True
            i=0
            while(flag):
                stream=b""
                line=b""
                while(line!=b"DELIMETER\n" and line!=b"END\n"):
                    stream+=line
                    line=serial_in.readline()
                    if(line==b"END\n"): flag=False
                if(flag):
                    cls.sources[i] = pickle.loads(stream)
                    i+=1
                    if(i%1000==0):print(i)
        return cls

    @classmethod
    def from_dict(cls, param_dict):
        cls=cls(size=param_dict["size"],
                catalog=param_dict["catalog"])
        return cls

    @property
    def g(self): #not ideal but ok for now
        return(s[g] for s in self.sources)
    @property
    def i(self): #not ideal but ok for now
        return(s[i] for s in self.sources)
    
if __name__=="__main__":
    #c=Catalog.from_pandas(filename="%s/pandas.test"%DATA)
    c=Catalog.from_pandas_to_array(filename="%s/pandas.test"%DATA)
    #c=Catalog.from_pandas_to_array(filename="%s/../initial/pandas_m33_2009.unique"%DATA)
    #c=Catalog.from_wfcam(filename="%s/wfcam.test"%DATA)
    #c=Catalog.from_pandas(filename="%s/../initial/pandas_m33_2009.unique"%DATA)

