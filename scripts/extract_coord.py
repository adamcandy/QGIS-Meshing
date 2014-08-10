#! /bin/python

import numpy as np
import NcTools
import sys
import os

def run(coord,filename,dstfile):
  filebase = filename[:-3]
  reader = NcTools.NcReader()
  reader.ncFile = filename
  reader.ReadFunc()

  if reader.typ == 'xr':
    os.system('module load gmt')
    os.system('grdmath %s 1 MUL = /tmp/tmpNcInputFile.nc')
    reader = NcTools.NcReader()
    reader.ncFile = '/tmp/tmpNcInputFile.nc'
    reader.ReadFunc()

  writer = NcTools.NcWriter()
  writer.ncFile = dstfile
  writer.typ = reader.typ
  writer.xvar = reader.x0
  writer.yvar = reader.x1
  
  if coord == '0':
    writer.phi = reader.x0
  elif coord == '1':
    writer.phi = reader.x1
  else:
    raise Exception

  writer.WriteFunc()


if __name__ == '__main__':
  sargs = sys.argv
  run(sargs[1],sargs[2],sargs[3])
