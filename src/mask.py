import numpy as np
import matplotlib.path as mpltpath
import Messier33

class ParentMask(object):
    """
    ParentMask not supposed to be directly accessed by user
    """
    def __init__(self, key, inverse=False):
        self.key=key
        self.index=[]
        self.inverse=inverse # keep values in index? (True,False)

    def generate_index(self, catalog):
        """
        INPUT:  catalog to mask
        FUNC:   Usually not user accessed, will generate cropping index without applying the crop 
        """

        #if(type(self.key)!=list):
            #if(self.key not in catalog.indices): raise ValueError("key='%s' not in catalog"%self.key)
        self._crop(catalog)
        if(self.inverse): self.index=self.invert_index(len(catalog))

    def apply_on(self, catalog, overwrite=False):
        """
        INPUT:  catalog on which to apply crop
                overwrite (False) will make copy of catalog if set to False
        RETURNS: copy of catalog with crop applied
        """
        self.generate_index(catalog)
        Messier33.info("*Cropping %d sources on key=%s\n"%(len(self.index),self.key))
        if(overwrite): 
            catalog.data = catalog.data[self.index]
            return(catalog)
        else:
            c = Messier33.DataBase.copy(catalog)
            c.data = catalog.data[self.index]
            return(c)

    def invert_index(self, n):
        mask = set(range(n))-set(self.index)
        return(list(mask))

    def __add__(self, mask):
        self.index = list( set(self.index)&set(mask.index))
        return(self)

    def plot(self, ax, **kwargs):
        pass

class Bool(ParentMask):
    def __init__(self, value, key, inverse=False):
        """
        INPUT:  value= value of which to mask
                key= which field to crop in 
                inverse = False will KEEP any catalog line matching value
                inverse = True will DISCARD any catalog line matching value
        """
        super(Bool, self).__init__(key,inverse)
        if(type(value)!=list): value=list(value)
        self.value=value

    def _crop(self, catalog):
        for i,value in enumerate(catalog[self.key]):
            if(value in self.value): self.index.append(i)

class Cut(ParentMask):
    def __init__(self, threshold, key, inverse=False):
        """
        INPUT:  value= cut threshold
                key= which field to crop in
                inverse=(False) defaults to cropping OUT values LESS than value. 
                inverse=True will cut values ABOVE threshold
        """
        super(Cut, self).__init__(key,inverse)
        self.threshold=threshold

    def _crop(self, catalog):
        for i,value in enumerate(catalog[self.key]):
            if(value>self.threshold): self.index.append(i)

    def plot(self, ax, axis=0, **kwargs):
        if(axis==0): ax.axvline(self.threshold, **kwargs)
        else: ax.axhline(self.threshold, **kwargs)

class Slice(ParentMask):
    def __init__(self, bounds, key, inverse=False):
        if( not (type(bounds)==list or type(bounds)==set) and len(bounds)!=2): raise ValueError("bounds must be (list,set) or dimensions (1,2)")
        super(Slice,self).__init__(key,inverse)
        self.bounds=bounds

    def _crop(self, catalog):
        for i,value in enumerate(catalog[self.key]):
            if(self.bounds[0]<value and value<self.bounds[1]): self.index.append(i)

    def plot(self, ax, axis=0, **kwargs):
        axline=ax.axvline if(axis==0) else ax.axhline
        axline(self.bounds[0], **kwargs)
        axline(self.bounds[1], **kwargs)
        

class Box(ParentMask):
    def __init__(self, bounds, keys, inverse=False):
        super(Box, self).__init__(keys, inverse)
        self.bounds=np.array(bounds).flatten()
        if(len(self.bounds)!=4): raise ValueError("bounds must contain 4 values, got shape %s"%np.shape(bounds))
        self.slices = [Slice(bounds[:2], keys[0], inverse), Slice(bounds[2:], keys[1], inverse)]

    def _crop(self, catalog):
        for mask_slice in self.slices:
            mask_slice.generate_index(catalog)
        self.index=list( set(self.slices[0].index) & set(self.slices[1].index))

    def plot(self, ax, axis=0, **kwargs):
        c=self.bounds #lazy bandit..
        x = 0 if(axis==0) else 1
        y = 1 if(axis==0) else 0
        corners = np.array([ (c[0],c[2]), (c[1],c[2]), (c[1], c[3]), (c[0], c[3]), (c[0], c[2])])
        ax.plot(corners[:,x], corners[:,y], **kwargs)

class Polygon(ParentMask):
    def __init__(self, bounds, keys, inverse=False):
        super(Polygon, self).__init__(keys, inverse)
        self.polygon = mpltpath.Path(bounds)
        self.bounds=np.array(bounds)

    def _crop(self, catalog):
        index = self.polygon.contains_points( catalog[self.key].T )
        self.index = np.arange(len(catalog))[index]

    def plot(self, ax, axis=0, **kwargs):
        x = 0 if(axis==0) else 1
        y = 1 if(axis==0) else 0
        
        newshape = self.bounds.shape+np.array([1,0])
        c = np.append(self.bounds, self.bounds[0]).reshape(newshape)
        ax.plot(c[:,x], c[:,y], **kwargs)

class Preset(Polygon):
    def __init__(self, filename="%s/include/stype_masks/test.mask"%Messier33.HOME, inverse=False):
        with open(filename, 'r') as raw:
            line = raw.readline().strip("\n").split(';')
        self.name=line[0]
        keys=line[1:3]
        points=  line[3:]
        arr_points = np.array(points, dtype=float).reshape((int(len(points)/2),2))
        super(Preset,self).__init__(arr_points, keys, inverse)

    def plot(self, ax, axis=0, **kwargs):
        label=self.name 
        if("label" in kwargs): 
            label=kwargs["label"]
            kwargs.pop("label")
        super().plot(ax,axis=axis, label=label, lw=1, **kwargs)


if(__name__=="__main__"):
    mask = Preset()
