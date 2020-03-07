import numpy as np
from astropy.io import fits
from photutils import isophote
from photutils.isophote import Ellipse
from photutils import EllipticalAperture
from Messier33 import inclination
import Messier33

with fits.open("/home/s1539878/data/mphys/ellipse/m33_i_mosaic.fits") as d:
    head=d[0].header
    data=d[0].data


x0=head["CRPIX1"]
y0=head["CRPIX2"]

#x1,y1 = np.unravel_index(np.argmax(data), data.shape)
x2,y2=(3013,2651)
PA=np.radians(112)
sma=500
e=np.cos(inclination)
print(e,PA)
geometry = isophote.EllipseGeometry(x2, y2, sma, e, PA)
print(geometry.__dict__)
#aper=EllipticalAperture((x2,y2),sma, sma*(1-e), PA) 

"""
fig,ax = plt.subplots(1)
plt.imshow(data)
plt.scatter(x2,y2)
aper.plot()
plt.show()
"""
ellipse = Ellipse(data, geometry, threshold=0.01)
#print(ellipse.fit_isophote(400))
isolist=ellipse.fit_image(300,50,2500, fix_pa=True)
print(isolist.sma)
isolist.to_table().to_pandas().to_csv("tmp")


