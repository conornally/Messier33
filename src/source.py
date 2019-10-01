import pickle
from Messier33.include.m33 import *
class Source(object):
    def __init__(self, skycoord=(0,0), coords=(0,0),  bandDATA={}, size=6):
        self.skycoord=skycoord
        self.coords=coords
        self.bandDATA=bandDATA
        self.len=size
        self.tmp = np.arange(len(self.bandDATA.keys()))

    def colour(self, band1, band2):
        #should i store this somewhere?
        return(self[band1]-self[band2])

    def __getitem__(self, key):
        return(self.bandDATA[key])

    def __len__(self):
        return(6)

    @property
    def serial(self):
        return(pickle.dumps(self))

if __name__=="__main__":
    x=  Source()

