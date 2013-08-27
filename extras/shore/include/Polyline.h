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
#ifndef POLYLINE_H
#define POLYLINE_H

#include <deque>
#include <set>
#include <string>

#include "Vertex.h"

/** Class to manage shoreline.
 */
class Polyline{
 public:
  Polyline(){}
  ~Polyline(){}

  /// Print out diagnostics
  void Diagnostics();
  
  /// Read in a shoreline from GMT's ASCII file.
  void ReadGMT(std::string filename);

  /// Read in a shoreline from GSHHS.
  void ReadGSHHS(std::string filename);

  /// Read in shoreline in GTS file.
  void ReadGTS(std::string filename,
               std::vector<double> &x, std::vector<double> &y, std::vector<double> &z,
               std::vector<int> &edges, std::vector<int> &edge_ids);
  
  /// Simplify the polyline
  void Simplify(double distance_to_edge);

  /// Write out shoreline in GMT's ASCII shoreline format.
  void WriteGMT(std::string basename);

  /// Write out shoreline in GTS ASCII format.
  void WriteGTS(std::string basename, double merge_distance);

  /// Write out shoreline in VTK polydata format.
  void WriteVTK(std::string basename);

  /// Get number of polygons.
  int GetNumberOfPolys();

  /// Turn on verbose mode
  static void VerboseOn();

  /// Turn off verbose mode
  static void VerboseOff();

 private:
  static bool verbose;
  std::deque< std::deque<Vertex> > polylines;
  static const unsigned GEOM_COAST = 0x4;    //    4
};

#endif
