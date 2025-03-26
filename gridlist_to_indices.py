#!/usr/bin/env python3
from sys import argv, exit
from netCDF4 import Dataset, Variable
from typing import TextIO

STD_LON = "longitude"
STD_LAT = "latitude"

ATTR_STD_NAME = "standard_name"

def die(msg):
    print(msg)
    exit(1)

def index_of(needle, haystack):
    for i in range(len(haystack)):
        if needle == haystack[i]:
            return i
    return -1

def get_variable_with_std_name(name: str, netcdf: Dataset) -> Variable:
    for var in netcdf.variables.values():
        if hasattr(var, ATTR_STD_NAME) and var.standard_name == name:
            return var
    die(f"No variable found in netCDF file with standard name '{name}'")

def traverse(gridlist: TextIO, netcdf: Dataset):
    var_lat = get_variable_with_std_name(STD_LAT, netcdf)
    var_lon = get_variable_with_std_name(STD_LON, netcdf)

    lons = var_lon[:]
    lats = var_lat[:]
    for line in gridlist:
        if len(line) < 1 or line == '\n':
            continue
        parts = line.split()
        if len(parts) < 2:
            die(f"Invalid line in gridlist: {line} (must have at least 2 space-separated values)")
        (lon, lat) = (parts[0], parts[1])

        ilon = index_of(float(lon), lons)
        ilat = index_of(float(lat), lats)

        # print(f"{lon} = {ilon}, {lat} = {ilat}")
        print(f"{ilon} {ilat}")

def main(gridlist: str, netcdf_file: str):
    with open(gridlist, "r") as gl:
        with Dataset(netcdf_file, "r") as nc:
            traverse(gl, nc)

if __name__ == "__main__":
    if len(argv) != 3:
        die(f"Usage: {argv[0]} <gridlist> <file.nc>")

    gridlist = argv[1]
    netcdf_file = argv[2]
    main(gridlist, netcdf_file)
