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
#include <cmath>
#include <cstdlib>

#include "Vertex.h"

using namespace std;

int Vertex::dimension=3;

Vertex::Vertex(){
  id = -1;
  flag = 0;
  lock = false;
}

Vertex::Vertex(const Vertex& v){
  *this = v;
}

Vertex::Vertex(int _id, double x, double y, double z){
  dimension = 3;
  id = _id;
  xyz[0] = x;
  xyz[1] = y;
  xyz[2] = z;
  flag = 0;
  lock = false;
}

Vertex::Vertex(int _id, double x, double y, double z, unsigned _flag){
  dimension = 3;
  id = _id;
  xyz[0] = x;
  xyz[1] = y;
  xyz[2] = z;
  flag = _flag;
  lock = false;
}

Vertex::Vertex(int _id, double x, double y){
  dimension = 2;
  id = _id;
  xyz[0] = x;
  xyz[1] = y;
  flag = 0;
  lock = false;
}

Vertex::Vertex(int _id, const double *_xyz, int _dimension){
  dimension = _dimension;
  id = _id;
  if((dimension==2)||(dimension==3)){
    cerr<<"ERROR: Only 2 and 3 dimensional vertices are supported.\n";
    exit(-1);
  }
  
  for(int i=0;i<dimension;i++){
    xyz[i] = _xyz[i];
  }
  
  flag = 0;
  lock = false;
}

Vertex::~Vertex(){}

void Vertex::AddFlag(unsigned _flag){
  flag = flag|_flag;
}
  
void Vertex::GetCoordinate(double &x, double &y, double &z){
  x = xyz[0];
  y = xyz[1];
  if(dimension==2)
    z = 0.0;
  else
    z = xyz[2];
}

void Vertex::GetCoordinate(double &x, double &y){
  assert(dimension==2);
  x = xyz[0];
  y = xyz[1];
}

void Vertex::GetCoordinate(double *_xyz){
  for(int i=0;i<dimension;i++){
    _xyz[i] = xyz[i];
  }
}

void Vertex::GetCoordinate2(double *_xyz){
  for(int i=0;i<2;i++){
    _xyz[i] = xyz[i];
  }
}

int Vertex::GetDimension() const{
  return dimension;
}

unsigned Vertex::GetFlag() const{
  return flag;
}

unsigned Vertex::GetID() const{
  return id;
}

double Vertex::GetX() const{
  return xyz[0];
}

double Vertex::GetY() const{
  return xyz[1];
}

double Vertex::GetZ() const{
  return xyz[2];
}

bool Vertex::IsBounded(const double *bbox){
  for(int i=0;i<dimension;i++)
    if((xyz[i]<bbox[i*2])||(xyz[i]>bbox[i*2+1]))
      return false;
  return true;
}

bool Vertex::IsBounded2(const double *bbox){
  for(int i=0;i<2;i++)
    if((xyz[i]<bbox[i*2])||(xyz[i]>bbox[i*2+1]))
      return false;
  return true;
}

bool Vertex::IsLocked(){
  return lock;
}

void Vertex::Lock(){
  lock = true;
}

void Vertex::SetCoordinate(double x, double y, double z){
  dimension = 3;
  xyz[0] = x;
  xyz[1] = y;
  xyz[2] = z;
}

void Vertex::SetCoordinate(double x, double y){
  dimension = 2;
  x = xyz[0];
  y = xyz[1];
}

void Vertex::SetCoordinate(const double *_xyz, int _dimension){
  dimension = _dimension;
  if((dimension!=2)&&(dimension!=3)){
    cerr<<"ERROR: Only 2 and 3 dimensional vertices are supported.\n";
    exit(-1);
  }
  
  for(int i=0;i<dimension;i++){
    xyz[i] = _xyz[i];
  }
}

void Vertex::SetFlag(unsigned _flag){
  flag = _flag;
}

void Vertex::SetX(double x){
  xyz[0] = x;
}

void Vertex::SetY(double y){
  xyz[1] = y;
}

void Vertex::SetZ(double z){
  xyz[2] = z;
}

void Vertex::SetID(int _id){
  id = _id;
}
 
void Vertex::Unlock(){
  lock = false;
}

ostream &operator<<(ostream& out, const Vertex& in){
  if(in.dimension==2)
    out<<in.xyz[0]<<" "<<in.xyz[1]<<endl;
  else
    out<<in.xyz[0]<<" "<<in.xyz[1]<<" "<<in.xyz[2]<<endl;
  return out;
}

Vertex &Vertex::operator=(const Vertex& in){
  dimension = in.dimension;
  id = in.id;
  flag = in.flag;
  lock = in.lock;
  for(int i=0;i<dimension;i++)
    xyz[i] = in.xyz[i];
  return *this;
}
