from Messier33.include.m33 import *
class Source:
    def __init__(self, skycoord=SkyCoord, bandDATA={}):
        self.skycoord=skycoord
        self.bandDATA=bandDATA
        self.len=len(self.bandDATA.keys())

    def __getitem__(self, key):
        return(self.bandDATA[key])

    def __len__(self):
        return(self.len)

if __name__=="__main__":
    x=  Source()

