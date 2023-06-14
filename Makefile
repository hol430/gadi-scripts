CFLAGS=-Wall -Werror -pedantic -O3 -fPIC
LDFLAGS=`pkg-config --libs netcdf` #-lnetcdf

all: ncmc
clean: $(RM) ncmc
ncmc: src/ncmc/ncmc.c
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

