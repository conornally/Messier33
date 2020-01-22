import Messier33
import numpy as np
cat=Messier33.Catalog.from_serialised("pandas.pickle")
cat.convert_to_stdcoords()
cat.deproject_radii()

cat.append(np.zeros(len(cat)),"shell")
l0=2.4
i=0
indexes=[]
while(l0<max(cat["dist"])):
    mask=Messier33.mask.Slice((l0,l0+0.1),"dist")
    mask.apply_on(cat)
    index=mask.index
    indexes.append(index)
    cat["shell"][index]=i
    l0+=0.1
    i+=1
print(cat["shell"])
print(cat[indexes[0]])

"""
so the layout could be:

    Radial_catalog( Catalog ): // this doesnt reeeeallly need to inherit
        
        >list of shell ranges
        >> masks to section off the main array
        cat[shells[i]]

"""
