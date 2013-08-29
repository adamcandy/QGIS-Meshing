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
    
    x0 = array(reader.x0)
    x1 = array(reader.x1)
    field = array(reader.phi)
    #issue with list length - as is over flat of domain
    if reader.typ == 'xr':
      spacex1 = reader.fnc.variables['spacing'][1]
      spacex0 = reader.fnc.variables['spacing'][0]

      startx1 = reader.fnc.variables['y_range'][0]
      startx0 = reader.fnc.variables['x_range'][0]

      endx1 = reader.fnc.variables['y_range'][1]
      endx0 = reader.fnc.variables['x_range'][1]

      nx0 = int((endx0 - startx0)/spacex0)
      nx1 = int((endx1 - startx1)/spacex1)

    elif reader.typ == 'll' or reader.typ == 'xy':
      #raw: x0,x1
      
      spacex0 = x0[0,1] - x0[0,0]
      spacex1 = x1[1,0] - x1[0,0]

      startx0 = x0[0,0]
      startx1 = x1[0,0]
   
      endx0 = x0[0,-1]
      endx1 = x1[-1,0]

      nx0 = x0.shape[1]
      nx1 = x1.shape[0]
      

    #degrees:
    pos_string = str(startx0)+" "+str(startx1)+" 0\n"
    pos_string += "%.8f" % spacex0+" "+ "%.8f" % spacex1+" 1\n"
    pos_string += str(nx0)+" "+str(nx1) + " 1\n"

    if reader.typ == 'xr':
      field.shape = [nx1,nx0]
      #field = fliplr(field)
      field = fliplr(transpose(field))
    else:
      field = transpose(field)
    
    pos_string += '\n'.join(map(str,abs(field.flatten()))) + '\n'

    return pos_string

def create_fld_file(netcdf_file,outfilename):
  pos_string = create_field(netcdf_file)

  f = open(outfilename,'w')
  f.write(pos_string)
  f.close()

if __name__ == "__main__":
    main()
