import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord

gx,gy,g,gerr,gcls=np.arange(5)+0
ix,iy,i,ierr,icls=np.arange(5)+5

def convert_to_dict(obj):
    obj_dict={  "__class__":obj.__class__.__name__,
                "__module__":obj.__module__}
    obj_dict.update(obj.__dict__)
    return(obj_dict)

def dict_to_obj(_dict):
    print(_dict)
    if("__class__"not in _dict): return(_dict)
    else:
        class_name=_dict.pop("__class__")
        module_name=_dict.pop("__module__")
        module=__import__(module_name)
        class_=getattr(module,class_name)
        return(class_(**_dict))


