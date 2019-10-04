CFLAGS	:= -w

#for now
bin/catalog_converter: src/catalog_converter.c
	gcc -o bin/catalog_converter src/catalog_converter.c

