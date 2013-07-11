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

#ifndef TVINCENTY_H
#define TVINCENTY_H

#include <cstdlib>

class TVincenty{
 public:
  TVincenty();
  ~TVincenty();
  
  static double EllipsoidalDistance(double lat1, double long1, double lat2, double long2);
  
 private:
  static const double pi, deg2rad;
  static double a,f,esq;

};

#endif
