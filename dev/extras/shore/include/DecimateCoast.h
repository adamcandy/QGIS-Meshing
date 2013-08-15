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

#ifndef DECIMATECOAST_H
#define DECIMATECOAST_H
class DecimateCoast;

#include <deque>
#include <map>
#include <set>
#include <string>

#include "Ellipsoid.h"
#include "Vertex.h"

class DecimateCoast{
public:
  DecimateCoast();
  void Decimate(std::deque<Vertex> &coast, bool trim=true);
  void SetError(double);
  void SphericalProjectionOn();
  void StereographicProjectionOn();
  void VerboseOn();
 private:
  DecimateCoast(const DecimateCoast&);
  DecimateCoast& operator=(const DecimateCoast&);
  
  inline double diagnostic(size_t v0, size_t v1, std::deque<Vertex>& coast) const;
  
  inline size_t find_best(size_t v0, size_t v1, size_t v2, std::deque<Vertex>&) const;
  
  inline std::map< size_t, std::deque<size_t> >::iterator find_next(std::map< size_t, std::deque<size_t> >::iterator node,
																	std::map< size_t, std::deque<size_t> >& shoreline,
																	bool cyclic) const;
  inline std::map< size_t, std::deque<size_t> >::iterator find_prev(std::map< size_t, std::deque<size_t> >::iterator node,
																	std::map< size_t, std::deque<size_t> >& shoreline,
																	bool cyclic) const;
  
  inline double get_d(double x,  double y,
					  double x1, double y1,
					  double x2, double y2) const;
  
  inline double get_length(size_t v0, size_t v1, std::deque<Vertex>& coast) const;
  inline double get_length(double x0, double y0, double x1, double y1) const;
  
  inline double GetDistToEdge(double, double) const;
  static size_t ncalls;
  
  double distance_to_edge;
  bool verbose;
};

#endif
