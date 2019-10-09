import numpy as np

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

        if(type(self.key)!=list):
            if(self.key not in catalog.indices): raise ValueError("key='%s' not in catalog"%self.key)
        self._crop(catalog)
        if(self.inverse): self.index=self.invert_index(len(catalog))

    def apply_on(self, catalog):
        """
        INPUT:  catalog on which to apply crop
        RETURNS: catalog with crop applied
        """
        self.generate_index(catalog)
        catalog._data = catalog._data[self.index]
        return(catalog)

    def invert_index(self, n):
        mask = set(range(n))-set(self.index)
        return(list(mask))

    def __add__(self, mask):
        self.index = list( set(self.index)&set(mask.index))
        return(self)

class Bool(ParentMask):
    def __init__(self, value, key, inverse=False):
        """
        INPUT:  value= value of which to mask
                key= which field to crop in 
                inverse = False will KEEP any catalog line matching value
                inverse = True will DISCARD any catalog line matching value
        """
        super(Bool, self).__init__(key,inverse)
        self.value=value

    def _crop(self, catalog):
        for i,value in enumerate(catalog[self.key]):
            if(value==self.value): self.index.append(i)

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

class Slice(ParentMask):
    def __init__(self, bounds, key, inverse=False):
        if( not (type(bounds)==list or type(bounds)==set) and len(bounds)!=2): raise ValueError("bounds must be (list,set) or dimensions (1,2)")
        super(Slice,self).__init__(key,inverse)
        self.bounds=bounds

    def _crop(self, catalog):
        for i,value in enumerate(catalog[self.key]):
            if(self.bounds[0]<value and value<self.bounds[1]): self.index.append(i)

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


        


if __name__=="__main__":
    import Messier33
    c = Messier33.Catalog.from_serialised("%s/data/test/pandas.pickle"%Messier33.ROOT)
    print(c['g'])

    #mask = Cut(0, 'g', inverse=True)
    mask = Slice( (10,20), 'g')
    c = mask.apply_on(c)
    print(c['g'])




