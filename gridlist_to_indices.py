#!/usr/bin/env python3
from sys import argv, exit
from netCDF4 import Dataset

VAR_LON = "longitude"
VAR_LAT = "latitude"

def index_of(needle, haystack):
    for i in range(len(haystack)):
        if needle == haystack[i]:
            return i
    return -1

if len(argv) != 3:
    print(f"Usage: {argv[0]} <gridlist> <file.nc>")
    exit(1)

gridlist = argv[1]
netcdf_file = argv[2]

def traverse(gridlist, netcdf):
    lons = netcdf.variables[VAR_LON][:]
    lats = netcdf.variables[VAR_LAT][:]
    for line in gridlist:
        if len(line) < 1 or line == '\n':
            continue
        (lon, lat) = line.split()

        ilon = index_of(float(lon), lons)
        ilat = index_of(float(lat), lats)

        # print(f"{lon} = {ilon}, {lat} = {ilat}")
        print(f"{ilon} {ilat}")
with open(gridlist, "r") as gl:
    with Dataset(netcdf_file, "r") as nc:
        traverse(gl, nc)
