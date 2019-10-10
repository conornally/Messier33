# Messier33
Code base for masters project - The Structure and Stellar Content of M33s outer Disk

## Basic Usage

```python
import Messier33

catalog=Messier33.Catalog.from_pandas("~data/pandas_catalog.cat")
catalog.crop(removing=(-1,0,-8)) # soon to be removed

catalog.convert_to_stdcoords()
catalog.deproject_radii()

mag, colour = catalog["g", "g-i"]

mask = Messier33.mask.Slice( (0.5,1.5), "dist")
catalog = mask.apply_on(catalog)

mask2=Messier33.mask.Polygon( [(0,0),(1,1),(0,1)], ["g", "g-i"])
cat_2 = mask2.apply_on(catalog) ##VERIFY this creates a copy?? i dont think it does

catalog.export("out.pickle")
catalog = Messier33.Catalog.from_serialised("out.pickle")

```
