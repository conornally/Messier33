import pickle,json

from matplotlib import use
use("Agg")
import matplotlib.pyplot as plt

from Messier33.include.m33 import *
from Messier33.include.config import *
from Messier33.src.source import Source
from Messier33.src.loading import Loading

class Catalog(object):
    def __init__(self, catalog="null", size=0, name="null"):
        #self.sources=[Source]*size
        #self.sources=np.array([Source()]*size)#, dtype=Source)
        self.sources = [Source]*size
        self.sources_array=None

        self.catalog=catalog
        self.name=name
        self.size=size

    @classmethod
    def from_pandas(cls, filename="%s/pandas_m33_2009.unique"%DATA):
        _size=cls.filelength(filename)
        cls=cls(catalog="pandas", size=_size, name=filename)
        load = Loading(_size)
        with open(filename, 'r') as raw:
            for i,line in enumerate(raw.readlines()[:]):
                splitline=cls.split_pandas_line(line, float)
                ra = cls.hms_to_degrees(*splitline[:3])
                dec= cls.dms_to_degrees(*splitline[3:6])
                _bandDATA=cls.list_to_bandINFO(splitline[6:11], band='g')
                _bandDATA.update(cls.list_to_bandINFO(splitline[11:16], band='i')) 
                cls.sources[i]=Source(coords=(ra,dec), bandDATA=_bandDATA)
                load(i)
        return cls

    @classmethod
    def from_wfcam(cls, filename="%s/wfcam_m33_lot.unique"%DATA):
        _size=cls.filelength(filename)
        cls=cls(catalog="wfcam", size=_size, name=filename)
        load = Loading(_size)
        with open(filename, 'r') as raw:
            for i,line in enumerate(raw.readlines()[:]):
                splitline=cls.split_wfcam_line(line, float)
                ra=cls.hms_to_degrees(*splitline[:3])
                dec=cls.dms_to_degrees(*splitline[3:6])
                _bandDATA=cls.list_to_bandINFO(splitline[7:12], band='J')
                _bandDATA.update(cls.list_to_bandINFO(splitline[12:17], band='K'))
                _bandDATA.update(cls.list_to_bandINFO(splitline[17:22], band='H'))
                cls.sources[i]=Source(coords=(ra,dec), bandDATA=_bandDATA)
                load(i)
        return cls

    @classmethod
    def from_pandas_to_array(cls, filename="%s/pandas_m33_2009.unique"%DATA):
        #will probably delete later
        _size=cls.filelength(filename)
        cls=cls(catalog="pandas", size=_size, name=filename)
        cls.sources_array=np.zeros((_size,18))
        with open(filename, 'r') as file_in:
            for i,line in enumerate(file_in.readlines()):
                cls.sources_array[i] = cls.split_pandas_line(line)#, dtype=float)) #float automatic
        return cls

    @staticmethod
    def split_pandas_line(line, dtype=str):
        splitline =[line[:3], line[3:6], line[6:12], 
                    line[12:16], line[16:19], line[19:24], 
                    line[24:31], line[31:38], line[38:45], line[45:52], line[52:55], 
                    line[55:62], line[62:69], line[69:76], line[76:83], line[83:86]]
                    #line[86:89], line[89:93]]
        return(list(dtype(x) for x in splitline))

    @staticmethod
    def split_wfcam_line(line, dtype=str):
        splitlist =[line[:3], line[3:6], line[6:13], 
                    line[13:17], line[17:20], line[20:27], 
                    line[27:30], 
                    line[30:37], line[37:44], line[44:51], line[52:58], line[58:61],
                    line[61:68], line[68:75], line[75:82], line[82:89], line[89:92],
                    line[92:99], line[99:106], line[106:113], line[113:120], line[120:123] ]
                    #line[86:89], line[89:93]]
        return(list(dtype(x) for x in splitlist))

    @staticmethod
    def line_to_skycoord(rawline): #this is very slow and SUPER memory intensive, i think ill convert to just float(degrees)
        ra="%s:%s:%s"%(rawline[0], rawline[1], rawline[2])
        dec="%s:%s:%s"%(rawline[3], rawline[4], rawline[5])
        return(SkyCoord(ra=ra,dec=dec,unit="deg"))

    @staticmethod
    def list_to_bandINFO(rawlist, band="g"):
        bandINFO={  "%s"%band: rawlist[2],
                    "d%s"%band:rawlist[3],
                    "%scls"%band:rawlist[4]}
        return(bandINFO)

    @staticmethod
    def filelength(filename):
        i=0
        with open(filename) as f:
            for i,l in enumerate(f): pass
        return i+1

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

    @staticmethod
    def dms_to_degrees(d,m,s):
        return(d+(m/60.0)+(s/3600.0))

    @staticmethod
    def hms_to_degrees(h,m,s):
        return((h*15.0)+(m/4.0)+(s/240.0))

    @property
    def g(self): #not ideal but ok for now
        return(s['g'] for s in self.sources)
    @property
    def i(self): #not ideal but ok for now
        return(s['i'] for s in self.sources)

    def colour(self, band1, band2):
        return( s.colour( band1, band2 ) for s in self.sources )

    def crop(self, removing=(1,0,-9,-8,-3), override=True):
        #ok this has some more work needed
        #it will only append once now, but if star not resolved in one band it might not fully be cropped
        _sources = []
        for source in self.sources:
            flag=True
            for cls in "giJKH":
                if(cls in source.bandDATA):
                    if(source["%scls"%cls] in removing): flag=False
            if(flag): _sources.append(source)
        if(override): self.sources=_sources
        self.name+=".cropped"
        return _sources

    def __len__(self):
        return(len(self.sources))

    def __getitem__(self, i):
        return(self.sources[i])

if __name__=="__main__":
    #c=Catalog.from_pandas(filename="%s/pandas.test"%DATA)
    #c=Catalog.from_pandas(filename="%s/../initial/pandas_m33_2009.unique"%DATA)
    #c=Catalog.from_pandas_to_array(filename="%s/pandas.test"%DATA)
    #c=Catalog.from_pandas_to_array(filename="%s/../initial/pandas_m33_2009.unique"%DATA)
    c=Catalog.from_wfcam(filename="%s/wfcam.test"%DATA)

    c.crop()
