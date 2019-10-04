"""
NAME
    fileio.py

SYNOPSIS
    API for file interaction through Messier33 
"""
import numpy as np
import pickle
from Messier33 import hms_to_degrees, dms_to_degrees

raw_dict = {"data":np.array,
            "style":"pandas",
            "size":(0,0),
            "indices":[] }

n_cols = {"pandas_raw":18, "wfcam_raw":22, "pandas_reduced":8, "wfcam_reduced":11}

def split_pandas_line(line, dtype=str):
    splitline =[line[:3], line[3:6], line[6:12], 
                line[12:16], line[16:19], line[19:24], 
                line[24:31], line[31:38], line[38:45], line[45:52], line[52:55], 
                line[55:62], line[62:69], line[69:76], line[76:83], line[83:86]]
    return(list(dtype(x) for x in splitline))

def split_wfcam_line(line, dtype=str):
    splitlist =[line[:3], line[3:6], line[6:13], 
                line[13:17], line[17:20], line[20:27], 
                line[27:30], 
                line[30:37], line[37:44], line[44:51], line[52:58], line[58:61],
                line[61:68], line[68:75], line[75:82], line[82:89], line[89:92],
                line[92:99], line[99:106], line[106:113], line[113:120], line[120:123] ]
    return(list(dtype(x) for x in splitlist))

def reduce_line_pandas(line):
    data = np.zeros(n_cols["pandas_reduced"])
    splitline = split_pandas_line(line, float)
    data[0] = hms_to_degrees(*splitline[:3])
    data[1] = dms_to_degrees(*splitline[3:6])
    data[2:5] = splitline[8:11]
    data[5:] = splitline[13:16]
    return data

def reduce_line_wfcam(line):
    data = np.zeros(n_cols["wfcam_reduced"])
    splitline = split_wfcam_line(line, float)
    data[0] = hms_to_degrees(*splitline[:3])
    data[1] = dms_to_degrees(*splitline[3:6])
    data[2:5] =splitline[9:12]
    data[5:8] =splitline[14:17]
    data[8:] = splitline[19:22]
    return data

def import_from_serialised(filename):
    with open(filename, "rb") as f:
        catalog_dict=pickle.load(f)
    return catalog_dict 

def import_from_raw(filename, style="pandas"):
    """
    INPUT:  Filename = str(filepath)
            style = pandas,wfcam
    FUNC:   Creates a dictionary of all useful values associated with this file
    RETURNS:info dictionary {'data','style','size','indices'}
    """
    _size = (filelength(filename), n_cols["%s_reduced"%style])
    data = np.zeros(_size)
    indices=raw_dict["indices"]
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if(style=="pandas"):
                data[i] = reduce_line_pandas(line)
                indices=["ra","dec","g","dg","gclc","i","di","icls"]
            if(style=="wfcam"):
                data[i] = reduce_line_wfcam(line)
                indices=["ra","dec","J","dJ","Jcls","H","dH","Hcls", "K", "dK", "Kcls"]
    return( {"data":data, "style":style, "size":_size, "indices":indices})

def filelength(filename):
    """
    INPUT:  Filename
    RETURN: number of file lines
    """
    i=0
    with open(filename) as f:
        for i,l in enumerate(f.readlines(),1):pass
    return(i)

def serialise(filename, catalog_dict={}):
    with open(filename, "wb") as f:
        pickle.dump(catalog_dict, f)

if __name__=="__main__":
    import Messier33
    x=import_from_raw(Messier33.DATA+"/wfcam.test", "wfcam")
    x.pop('data')
    print(x)
