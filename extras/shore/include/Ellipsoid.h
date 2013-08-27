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

#ifndef ELLIPSOID_H
#define ELLIPSOID_H

#include <cassert>
#include <iostream>
#include <cmath>
#include <string>

class Ellipsoid{
 public:
  Ellipsoid();
  static double get_ds2(double, double, double, double);
  static void get_llz(double, double, double, double &, double &, double &);
  static void get_xyz(double, double, double, double &, double &, double &);
  static void setReferenceEllipsoid(std::string);
  static void VerboseOn();
  static void VerboseOff();
  static const char* ellipses[];

 private:
  static bool verbose;
  static std::pair<std::string, std::string> reference_ellipsoid;
  static const double pi, rad_to_deg, deg_to_rad;

  // Oblate spheroid
  static double a, a2, c2, sinh_xi, sinh_xi2, cosh_xi, cosh_xi2;
  
  // Spherical coordinates
  static const double earth_radius;
};

#endif
