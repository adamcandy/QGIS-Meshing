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

#include <cmath>
#include <cstring>

#include <iostream>

#include "TVincenty.h"
#include "Ellipsoid.h"

extern "C" {
  void elipss_(char *, double *, double *);
  void gpnhri_(const double *a, const double *f, const double *esq, const double *pi,
               const double *p1, const double *e1, const double *p2, const double *e2,
               double *faz, double *baz, double *edist);
}


// Declare static members
const double TVincenty::pi=4.0*atan(1.0);
const double TVincenty::deg2rad = pi/180.0;

// Set the default as '1' - GRS80 / WGS84  (NAD83)
double TVincenty::a = 6378137.0;
double TVincenty::f = 1.0/298.25722210088;
double TVincenty::esq = f*(2.0-f);

using namespace std;

TVincenty::TVincenty(){}
TVincenty::~TVincenty(){}

double TVincenty::EllipsoidalDistance(double lat1, double long1, double lat2, double long2){
  //<debugging>
  // double ds = sqrt(Ellipsoid::get_ds2(long1, lat1, long2, lat2));
  //</debugging>

  double p1 = lat1*deg2rad;
  double e1 = long1*deg2rad;
  double p2 = lat2*deg2rad;
  double e2 = long2*deg2rad;

  //<debugging>
  //double average_r = 6372795.477598;
  //double ds_sphere = average_r*acos( sin(p1-PI/2)*sin(p2-PI/2)*cos(e1)*cos(e2) +
  //				     sin(p1-PI/2)*sin(p2-PI/2)*sin(e1)*sin(e2) +
  //				     cos(p1-PI/2)*cos(p2-PI/2) );
  //</debugging>

  if(e1<0.0)
    e1+=2.0*pi;
  
  if(e2<0.0)
    e2+=2.0*pi;
   
  // compute the geodetic inverse
  double faz;   // forward azimuth
  double baz;   // backward azimuth
  double edist; // Ellipsoidal distance - meters
  gpnhri_(&a,&f,&esq,&pi,&p1,&e1,&p2,&e2,&faz,&baz,&edist);

  if(!finite(edist)){
    cerr<<"Ellipsoidal distance = "<<edist<<endl
	<<"("<<long1<<", "<<lat1<<"), "
	<<"("<<long2<<", "<<lat2<<")"<<endl;
    exit(-1);
  }
  
  //cout<<"Ds "<<edist<<" "
  //   <<ds<<" "<<" "<<fabs(ds-edist)<<" "
  //   <<ds_sphere<<" "<<" "<<fabs(ds_sphere-edist)<<endl;
  return edist;    
}
