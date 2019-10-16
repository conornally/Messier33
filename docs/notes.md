# general notes for the code base

loading catalog takes too long!
>   it will be smaller once i recieve cropped catalog
>   i will try to serialise the catalog to reload it faster
>	it doesnt do great on "big" files, might try my own serialisation methods, might be faster or less memory/cpu intensive

unit testing
>	need to get this started before data structure becomes too big
>>>	total revamp of underlying data structure has screwed up my unit testing...

conversion to c++???
>	thatd be cool but is it worth trading run speed for dev time?

inclusion of scripts into API??
>	i could put the colour_mag etc. and catalogconverter scripts in here?

pickle still seems to have trouble with loading the bigger files

## current task

add Catalog.replace
[[add Catalog.insert]]
incorporate to Catalog.dust_correction


