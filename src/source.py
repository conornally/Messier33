from Messier33.include.m33 import *
class Source(object):
    def __init__(self, skycoord=None, bandDATA={}):
        self.skycoord=skycoord
        self.bandDATA=bandDATA
        self.len=len(self.bandDATA.keys())

    def __getitem__(self, key):
        return(self.bandDATA[key])

    def __len__(self):
        return(self.len)

    def __repr__(self):
        return("%s"%self.bandDATA)

if __name__=="__main__":
    x=  Source()

