# Messier33
Code base for masters project - The Structure and Stellar Content of M33s outer Disk

## Basic Usage

```python
import Messier33
catalog=Messier33.Catalog.from_pandas("~data/pandas_catalog.cat")
catalog.crop(removing=(-1,0,-8), override=True)
g_mag = catalog.g
g_i = catalog.colour("g", "i")
```
