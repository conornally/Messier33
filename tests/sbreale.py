import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils import isophote
from photutils.isophote import Ellipse
from photutils import EllipticalAperture
from Messier33 import inclination
import astropy.visualization as vis

with fits.open("/mnt/sd/data/m33/ellipse/m33_i_mosaic.fits") as d:
    head=d[0].header
    data=d[0].data

#print(repr(head))

x0=head["CRPIX1"]
y0=head["CRPIX2"]

x1,y1 = np.unravel_index(np.argmax(data), data.shape)
x2,y2=(3000,2600)
PA=np.radians(head["ROTSKYPA"])
sma=200
e=sma*(1-np.cos(inclination))
print(PA, head["ROTSKYPA"])
geometry = isophote.EllipseGeometry(x2, y2, sma, e, PA)
aper=EllipticalAperture((x2,y2),sma, e, PA) 
#aper = EllipticalAperture((geometry.x0, geometry.y0), geometry.sma, geometry.sma*(1 - geometry.eps), geometry.pa)
fig,ax = plt.subplots(1)
ax.imshow(data)
ax.scatter(x0,y0)
ax.scatter(x1,y1)
ax.scatter(y1,x1)
ax.scatter(x2,y2)
aper.plot(ax)
print(aper)
print(data[x1,y1])
plt.show()
#quit()

ellipse = Ellipse(data, geometry)
print(ellipse.fit_isophote(geometry.sma))
#isolist=ellipse.fit_image(100,0,1000)

