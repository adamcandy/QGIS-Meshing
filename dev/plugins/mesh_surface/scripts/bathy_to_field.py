#!/usr/bin/env python

import string
import re 
import os
import argparse
from numpy import *
#from Scientific.IO import NetCDF
from NcTools import NcReader
#import GFD_basisChange_tools as rot

def main():


    parser = argparse.ArgumentParser(
         description="""Convert a NetCDF file into a GMSH field (ASCII).
                      """
                     )

    parser.add_argument(
            '-v', 
            '--verbose', 
            action='store_true', 
            help="Verbose output: mainly progress reports",
            default=False
            )
    parser.add_argument(
            'input_netcdf',
            help="The input bathymetry file in netcdf format. The bathymetry should be called z"
            )
    parser.add_argument(
            'output',
            help="The output.dat file"
            )
    
    args = parser.parse_args()
    output_file = str(args.output)
    input_file = str(args.input_netcdf)
    verbose = args.verbose

    # Check arguments
    if (not os.path.exists(input_file)):
        print "Your input NetCDF file does not exist or you don't have permissions to read it"
        sys.exit(-1) 
    
    create_fld_file(input_file,output_file)

    return 0

def create_field(netcdf_file):

    # read netcdf file
    reader = NcReader()
    reader.ncFile = netcdf_file
    reader.ReadFunc()

    x0 = list(reader.x0) 
    x1 = list(reader.x1)
    field = array(reader.phi)
    #issue with list length - as is over flat of domain

    spacelat = reader.fnc.variables['spacing'][1]
    spacelon = reader.fnc.variables['spacing'][0]

    startlat = reader.fnc.variables['y_range'][0]
    startlon = reader.fnc.variables['x_range'][0]

    endlat = reader.fnc.variables['y_range'][1]
    endlon = reader.fnc.variables['x_range'][1]

    nLat = int((endlon - startlon)/spacelon)
    nLon = int((endlat - startlat)/spacelat)

    #degrees:
    pos_string = str(startlon)+" "+str(startlat)+" 0\n"
    pos_string += "%.8f" % spacelon+" "+ "%.8f" % spacelat+" 1\n"
    pos_string += str(nLat)+" "+str(nLon)+" 1\n"

    print field.flatten()
    field.shape = [nLon,nLat]
    field = fliplr(transpose(field))
    pos_string += '\n'.join(map(str,abs(field.flatten()))) + '\n'

    return pos_string

def create_fld_file(netcdf_file,outfilename):
  pos_string = create_field(netcdf_file)

  f = open(outfilename,'w')
  f.write(pos_string)
  f.close()

if __name__ == "__main__":
    main()
