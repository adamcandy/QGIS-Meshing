#!/usr/bin/env python

import numpy
import argparse
import os
import math
from Scientific.IO import NetCDF

def main():


    parser = argparse.ArgumentParser(
         prog="gaussian_bump",
         description="""Create a Gaussian bump in a netcdf file"""
         )


    parser.add_argument(
            '-v', 
            '--verbose', 
            action='store_true', 
            help="Verbose output: mainly progress reports.",
            default=False
            )
    parser.add_argument(
            '-d',
            '--domain',
            help="Domain size. Defualt is 1000x1000m",
            default=1000.0,
            type=float
            )
    parser.add_argument(
            '-b',
            '--bumpheight',
            help="Distance between seabed and top of bump. Default is 100m",
            default=100,
            type=float
            )
    parser.add_argument(
            '-r',
            '--resolution',
            help="Resolution of output netcdf file. Default is 10m",
            default=10.0,
            type=float
            )
    parser.add_argument(
            '--shift',
            help="Shift the bump in the 'north-south' direction, wrapping along the top/bottom",
            default = 0,
            type=float
            )
    parser.add_argument(
            '--spread',
            help="Spread of Gaussian",
            default = 100.0,
            type=float
            )
    parser.add_argument(
            'output_file', 
            metavar='output_file',
            nargs=1,
            help='The output netcdf file'
            )
    args = parser.parse_args() 
    verbose = args.verbose
    output_file = args.output_file[0]
    domain_size = args.domain
    bump_height = args.bumpheight
    resolution = args.resolution
    shift = args.shift
    spread = args.spread  

    nPoints = int(domain_size / resolution)
    shift = int(shift/resolution)
    if (verbose):
        print nPoints, shift
    
    # generate regular grid
    X, Y = numpy.meshgrid(numpy.linspace(0.0, domain_size, nPoints), numpy.linspace(0.0, domain_size, nPoints))
    Z = numpy.zeros((nPoints,nPoints))
    #for each point calculate the Gaussian
    centre = domain_size/2.0
    for i in range(0,len(X)):
        for j in range(0,len(X[0])):
            r = ((X[i][j]-centre)**2/(2.0*spread**2) + (Y[i][j]-centre)**2/(2.0*spread**2))
            Z[i][j] = bump_height * math.exp(-1.0*r)
            
    if (not shift == 0.0):
        Z = numpy.roll(Z, shift, 0)

    f = NetCDF.NetCDFFile(output_file, 'w')
    xDim = f.createDimension("X", nPoints)
    yDim = f.createDimension("Y", nPoints)
    x = f.createVariable("X","d",("X",))
    y = f.createVariable("Y","d",("Y",))
    zVar = f.createVariable("Z","d",("X","Y"))

    x.assignValue(X[0,0:nPoints])
    y.assignValue(Y[0:nPoints,0])
    zVar.assignValue(Z)

    f.close()

    os.system('grdreformat '+output_file+' '+output_file)
    os.system('rm -f 1_contour.* 50_contour.*')
    os.system('gdal_contour -fl 1.0 NETCDF:"'+output_file+'":z 1_contour.shp')
    os.system('gdal_contour -fl 50.0 NETCDF:"'+output_file+'":z 50_contour.shp')

if __name__ == "__main__":
    main()

