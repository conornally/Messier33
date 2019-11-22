import Messier33
c=Messier33.Catalog.from_pandas("test.pandas")
c2=Messier33.Catalog.from_wfcam("test.wfcam")
c3=Messier33.Catalog.from_serialised("pandas.pickle")

print(c['g'][0])
c.apply_distance_modulus(100,200)
print(c['g'][0])
c.extinction_correct()
print(c['go'][0])
