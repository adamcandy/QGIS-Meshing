/*
 *      Copyright (c) 2004-2006 by Gerard Gorman
 *      Copyright (c) 2006- Imperial College London
 *      See COPYING file for copying and redistribution conditions.
 *
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; version 2 of the License.
 *
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *
 *      Contact info: gerard.j.gorman@gmail.com/g.gorman@imperial.ac.uk
 */

#include <cassert>
#include <cerrno>
#include <cstdio>
#include <cstdlib>

#include <map>
#include <vector>

#include "confdefs.h"

#include "Polyline.h"

using namespace std;

void usage(char *prog){
  cerr<<"Usage:\n"
      <<prog<<" [<options>] infile\n"

      <<"The infile should be in GMT ASCII format, e.g. http://www.ngdc.noaa.gov/mgg/coast/\n"

      <<" -d <distance_to_edge>\n"
      <<" Feature length decimation "
      <<"threshold, the minimum edge length and the maximum edge length allowed along the coast. Feature "
      <<"error is calculated as the minimum of the distance-to-edge and the edge "
      <<"lengths connected to the node being considered for decimation. (default: 0.0)\n"

      <<" -h\n"
      <<" Prints this help message.\n"

      <<" -p\n"
      <<" Output VTK plots of various components of the mesh as meshing "
      <<"progresses.\n"

      <<" -v\n"
      <<" Verbose progress information. (default: off)\n"

      << endl;
}

int main(int argc, char **argv){
  double distance_to_edge = 0.0;

  bool verbose = false;
  bool do_vtk_plots = false;

  // Get any command line arguments reset optarg so we can detect
  // changes
  optarg = NULL;
  
  int getopt_c;
  while ((getopt_c = getopt(argc, argv, "d:hpv")) != EOF){
    char c = (char)getopt_c;
    switch(c){
    case 'd':
      distance_to_edge = atof(optarg);
      break;
    case 'h':
      usage(argv[0]);
      exit(0);
    case 'p':
      do_vtk_plots = true;
      break;
    case 'v':
      verbose = true;
      break;
    default:
      if (isprint(optopt)){
	cerr << "Unknown option " << optopt << endl;
      }else{
	cerr << "Unknown option " << hex << optopt << endl;
      }
      exit(-1);
    }
  }  

  // Calculate/read in shoreline
  Polyline polylines;

  if(verbose)
    polylines.VerboseOn();

  if(verbose) 
    cout<<"Reading ascii shoreline\n";

  polylines.ReadGMT(string(argv[argc-1]));
  
  if(do_vtk_plots)
    polylines.WriteVTK("original_shore");
  
  if(verbose)
    cout<<"Coarsen coast\n";
    
  polylines.Simplify(distance_to_edge);
  
  polylines.WriteGMT("shore");
  polylines.WriteVTK("shore");

  return 0;
}
