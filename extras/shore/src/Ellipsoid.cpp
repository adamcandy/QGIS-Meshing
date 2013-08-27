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

#include "Ellipsoid.h"

using namespace std;

bool Ellipsoid::verbose=false;
const double Ellipsoid::pi=4.0*atanl(1.0);
const double Ellipsoid::rad_to_deg=180.0/pi;
const double Ellipsoid::deg_to_rad=pi/180.0;

// Oblate spheroidal coordinates
double Ellipsoid::a=-1.0;
double Ellipsoid::a2=-1.0;
double Ellipsoid::c2=-1.0;
double Ellipsoid::cosh_xi=-1.0;
double Ellipsoid::cosh_xi2=-1.0;
double Ellipsoid::sinh_xi=-1.0;
double Ellipsoid::sinh_xi2=-1.0;

// Spherical coordinates
const double Ellipsoid::earth_radius=6378000;

const char *Ellipsoid::ellipses[]={"MERIT", "SGS85", "GRS80", "IAU76", "airy", "APL4.9", "NWL9D", \
                                   "mod_airy", "andrae", "aust_SA", "GRS67", "bessel", "bess_mod", \
                                   "bess_nam", "clrk58", "clrk66", "clrk66M", "clrk80", "clrk80M", \
                                   "clrk80B", "clrk80I", "clrk80R", "clrk80S", "CPM", "delmbr", \
                                   "engelis", "evrst30", "evrst48", "evrst56", "evrst69", "evrstSS", \
                                   "fschr60", "fschr60m", "fschr68", "GEM10C", "helmert", "hough", \
                                   "ind_NS", "intl", "krass", "kaula", "lerch", "new_intl", "OSU86F", \
                                   "OSU91A", "plessis", "SEasia", "struve", "walbeck", "waroff", "WGS60", \
                                   "WGS66", "WGS72", "WGS84", NULL};

pair<string, string> Ellipsoid::reference_ellipsoid;

Ellipsoid::Ellipsoid(){
  VerboseOff();
}

#include "TVincenty.h"

double Ellipsoid::get_ds2(double longitude1, double latitude1, double longitude2, double latitude2){
  longitude1*=deg_to_rad;
  longitude2*=deg_to_rad;
  
  double dlong = longitude1-longitude2;
  double dlong2 = dlong*dlong;
    
  double ds2=0;
  if(a<0){
    // Spherical polar coordinate
    double colatitude1 = (90.0 - latitude1)*deg_to_rad;
    double colatitude2 = (90.0 - latitude2)*deg_to_rad;
    
    double dlat = fabs(colatitude1-colatitude2);
    double dlat2 = dlat*dlat;
    
    double sin_lat = sin((colatitude1+colatitude2)*0.5);
    double sin_lat2 = sin_lat*sin_lat;
    
    ds2 = earth_radius*earth_radius*(dlat2 + sin_lat2*dlong2);
  }else{
    //Oblate spheroidal coordinates
    latitude1 = latitude1*deg_to_rad;
    latitude2 = latitude2*deg_to_rad;
    
    double dlat = fabs(latitude1-latitude2);
    double dlat2 = dlat*dlat;
    
    double sin_lat = sin((latitude1+latitude2)*0.5);
    double sin_lat2 = sin_lat*sin_lat;

    double cos_lat = cos((latitude1+latitude2)*0.5);
    double cos_lat2 = cos_lat*cos_lat;
    
    ds2 = a2*((sinh_xi2+sin_lat2)*dlat2 + cosh_xi2*cos_lat2*dlong2);
  }
  
  return ds2;
}

void Ellipsoid::get_llz(double x, double y, double z, double &longitude, double &latitude, double &_z){
  if(verbose)
    cout<<"void Ellipsoid::get_llz("
	<<x<<", "<<y<<", "<<z<<", longitude, latitude, depth)"<<endl;
  
  if(a<0){ // Spherical coordinates
    double r = sqrt(x*x+y*y+z*z);
    longitude = atan2(y, x);
    latitude = acos(z/r);
    _z = earth_radius - r;
  }else{
    longitude = atan2(y, x);
    latitude = atan(cos(longitude)*z*cosh_xi/(sinh_xi*x));
    if(latitude<0.0)
      latitude=pi+latitude;
    
    _z = z/(sinh_xi*sin(latitude)) - a;
  }  
  longitude*=rad_to_deg;
  latitude = 90 - latitude*rad_to_deg;
}

void Ellipsoid::get_xyz(double longitude, double latitude, double _z, double &x, double &y, double &z){
  if(verbose)
    cout<<"void Ellipsoid::get_xyz("
	<<longitude<<", "<<latitude<<", "<<_z<<", "
	<<"x, y, z)"<<endl;
  assert((latitude<=90)&&(latitude>=-90));
  
  // remember co-latitude
  longitude*=deg_to_rad;
  double colatitude = (90-latitude)*deg_to_rad;

  if(a<0){ // Spherical polar coordinates
    x = (earth_radius+_z)*sinl(colatitude)*cosl(longitude);
    y = (earth_radius+_z)*sinl(colatitude)*sinl(longitude);
    z = (earth_radius+_z)*cosl(colatitude);
  }else{ // Oblate spheroidal coordinates    
    x = (a+_z)*cosh_xi*cosl(latitude)*cosl(longitude);
    y = (a+_z)*cosh_xi*cosl(latitude)*sinl(longitude);
    z = (a+_z)*sinh_xi*sinl(latitude);
  }
  
  return;
}

void Ellipsoid::setReferenceEllipsoid(string ellipsoid){
  if(verbose)
    cout<<"void Ellipsoid::setReferenceEllipsoid("<<ellipsoid<<")\n";
  
  double b=-1.0;
  if(ellipsoid=="MERIT"){
    a=6378137.0;
    double rf=298.257;
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "MERIT 1983");
  }else if(ellipsoid=="SGS85"){
    a=6378136.0;
    double rf=298.257;
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Soviet Geodetic System 85");
  }else if(ellipsoid=="GRS80"){
    a=6378137.0;
    double rf=298.257222101;
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "GRS 1980(IUGG 1980)");
  }else if(ellipsoid=="IAU76"){
    a=6378140.0; 
    double rf=298.257; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "IAU 1976");
  }else if(ellipsoid=="airy"){
    a=6377563.396;
    b=6356256.910;
    reference_ellipsoid = pair<string, string>(ellipsoid, "Airy 1830");
  }else if(ellipsoid=="APL4.9"){
    a=6378137.0; 
    double rf=298.25;
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Appl. Physics. 1965");
  }else if(ellipsoid=="NWL9D"){
    a=6378145.0; 
    double rf=298.25; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Naval Weapons Lab. 1965");
  }else if(ellipsoid=="mod_airy"){
    a=6377340.189; 
    b=6356034.446; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Modified Airy");
  }else if(ellipsoid=="andrae"){
    a=6377104.43; 
    double rf=300.0;
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Andrae 1876 (Den. Iclnd.)");
  }else if(ellipsoid=="aust_SA"){
    a=6378160.0; 
    double rf=298.25;
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Aust. Natl & S. Amer. 1969 Intl 67");
  }else if(ellipsoid=="GRS67"){
    a=6378160.0; 
    double rf=298.2471674270; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "GRS 67(IUGG 1967)");
  }else if(ellipsoid=="bessel"){
    a=6377397.155; 
    double rf=299.1528128; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Bessel 1841");
  }else if(ellipsoid=="bess_mod"){
    a=6377492.018; 
    double rf=299.15281; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Bessel Modified");
  }else if(ellipsoid=="bess_nam"){
    a=6377483.865; 
    double rf=299.1528128; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Bessel 1841 (Namibia)");
  }else if(ellipsoid=="clrk58"){
    a=6378293.639; 
    b=6356617.981; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clark 1858");
  }else if(ellipsoid=="clrk66"){
    a=6378206.4; 
    b=6356583.8; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1866");
  }else if(ellipsoid=="clrk66M"){
    a=6378693.704; 
    b=6357069.451; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1866 Michigan");
  }else if(ellipsoid=="clrk80"){
    a=6378249.145; 
    b=6356514.960; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1880 (Arc)");
  }else if(ellipsoid=="clrk80M"){
    a=6378249.139; 
    double rf=293.4663; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1880");
  }else if(ellipsoid=="clrk80B"){
    a=6378300.79; 
    b=6356566.43; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1880 (Benoit)");
  }else if(ellipsoid=="clrk80I"){
    a=6378249.2; 
    double rf=293.46602; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1880 (IGN)");
  }else if(ellipsoid=="clrk80R"){
    a=6378249.145; 
    double rf=293.465; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1880 (RGS)");
  }else if(ellipsoid=="clrk80S"){
    a=6378249.2; 
    double rf=293.46598; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Clarke 1880 (SGA 1922)");
  }else if(ellipsoid=="CPM"){
    a=6375738.7; 
    double rf=334.29; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Comm. des Poids et Mesures 1799");
  }else if(ellipsoid=="delmbr"){
    a=6376428.; 
    double rf=311.5; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Delambre 1810 (Belgium)");
  }else if(ellipsoid=="engelis"){
    a=6378136.05; 
    double rf=298.2566; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Engelis 1985");
  }else if(ellipsoid=="evrst30"){
    a=6377276.345; 
    double rf=300.8017; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Everest 1830 (1937 adj.)");
  }else if(ellipsoid=="evrst48"){
    a=6377304.063; 
    double rf=300.8017; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Everest 1948");
  }else if(ellipsoid=="evrst56"){
    a=6377301.243; 
    double rf=300.8017; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Everest 1956");
  }else if(ellipsoid=="evrst69"){
    a=6377295.664; 
    double rf=300.8017; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Everest 1969");
  }else if(ellipsoid=="evrstSS"){
    a=6377298.556; 
    double rf=300.8017; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Everest (Sabah & Sarawak)");
  }else if(ellipsoid=="fschr60"){
    a=6378166.; 
    double rf=298.3; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Fischer (Mercury Datum) 1960");
  }else if(ellipsoid=="fschr60m"){
    a=6378155.; 
    double rf=298.3; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Modified Fischer 1960");
  }else if(ellipsoid=="fschr68"){
    a=6378150.; 
    double rf=298.3; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Fischer 1968");
  }else if(ellipsoid=="GEM10C"){
    a=6378137.0; 
    double rf=298.25722; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "GEM 10C grav model");
  }else if(ellipsoid=="helmert"){
    a=6378200.; 
    double rf=298.3; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Helmert 1906");
  }else if(ellipsoid=="hough"){
    a=6378270.0; 
    double rf=297.; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Hough");
  }else if(ellipsoid=="ind_NS"){
    a=6378160.0; 
    double rf=298.247; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Indonesian Natl. Sphrd");
  }else if(ellipsoid=="intl"){
    a=6378388.0; 
    double rf=297.; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "International 1909 (Hayford)");
  }else if(ellipsoid=="krass"){
    a=6378245.0; 
    double rf=298.3; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Krassovsky 1940");
  }else if(ellipsoid=="kaula"){
    a=6378163.; 
    double rf=298.24; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Kaula 1961");
  }else if(ellipsoid=="lerch"){
    a=6378139.; 
    double rf=298.257; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Lerch 1979");
  }else if(ellipsoid=="new_intl"){
    a=6378157.5; 
    b=6356772.2; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "New International 1967");
  }else if(ellipsoid=="OSU86F"){
    a=6378136.2; 
    double rf=298.25722; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "OSU86 grav. model");
  }else if(ellipsoid=="OSU91A"){
    a=6378136.3; 
    double rf=298.25722; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "OSU91 grav. model");
  }else if(ellipsoid=="plessis"){
    a=6376523.; 
    b=6355863.; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Plessis 1817 (France)");
  }else if(ellipsoid=="SEasia"){
    a=6378155.0; 
    b=6356773.3205; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Southeast Asia");
  }else if(ellipsoid=="struve"){
    a=6378297.; 
    double rf=294.73; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "Struve 1860");
  }else if(ellipsoid=="walbeck"){
    a=6376896.0; 
    b=6355834.8467; 
    reference_ellipsoid = pair<string, string>(ellipsoid, "Walbeck");
  }else if(ellipsoid=="waroff"){
    a=6378300.583; 
    double rf=296.; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "War Office");
  }else if(ellipsoid=="WGS60"){
    a=6378165.0; 
    double rf=298.3; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "WGS 60");
  }else if(ellipsoid=="WGS66"){
    a=6378145.0; 
    double rf=298.25; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "WGS 66 NWL 9D");
  }else if(ellipsoid=="WGS72"){
    a=6378135.0;
    double rf=298.26; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "WGS 72 NWL 10D");
  }else if(ellipsoid=="WGS84"){
    a=6378137.0; 
    double rf=298.257223563; 
    b=a*(1-1.0/rf);
    reference_ellipsoid = pair<string, string>(ellipsoid, "WGS 84");
  }else{
    cout.flush();
    cerr<<__FILE__<<", "<<__LINE__<<": ERROR - no such reference sphere, "<<ellipsoid<<endl; 
    exit(-1);
  }
  assert(a>0);
  assert(b>0);
  
  double xi = atanh(b/a);
  
  cosh_xi = cosh(xi);
  cosh_xi2 = cosh_xi*cosh_xi;
  
  sinh_xi = sinh(xi);
  sinh_xi2 = sinh_xi*sinh_xi;
  
  a2 = a*a;
  c2 = a2/cosh_xi2;
}

void Ellipsoid::VerboseOn(){
  verbose=true;
}

void Ellipsoid::VerboseOff(){
  verbose=false;
}
