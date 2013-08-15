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
 *      + reads ASCII shoreline
 *      + reads GSHHS dataset
 *
 *      Contact info: gerard.j.gorman@gmail.com/g.gorman@imperial.ac.uk
 */
#ifndef VERTEX_H
#define VERTEX_H

#include <iostream>
#include <ostream>

/** Basic class to store and operate on vertices.
 */
class Vertex{
 public:
  /// Default constructor.
  Vertex();

  /// Copy constructor.
  Vertex(const Vertex& Vertex);

  /// Coordinate  constructor.
  Vertex(int id, double x, double y, double z);

  /// Coordinate  constructor.
  Vertex(int id, double x, double y, double z, unsigned flag);

  /// Coordinate  constructor.
  Vertex(int id, double x, double y);

  /// Coordinate  constructor.
  Vertex(int id, const double *xyz, int dimension);

  /// Destructor.
  ~Vertex();

  /// Add flag
  void AddFlag(unsigned flag);

  /// Get the coordinate.
  void GetCoordinate(double &x, double &y, double &z);

  /// Get the coordinate.
  void GetCoordinate(double &x, double &y);

  /// Get the coordinate.
  void GetCoordinate(double *xyz);

  /// Get the 2-d coordinate (ignore z if it exists).
  void GetCoordinate2(double *xyz);

  // Get the dimension
  int GetDimension() const;

  /// Get flag
  unsigned GetFlag() const;

  /// Get id
  unsigned GetID() const;

  /// Get the tolerance used for floating point comparisons.
  static double GetTolerance();

  /// Get X value
  double GetX() const;

  /// Get Y value
  double GetY() const;

  /// Get Z value
  double GetZ() const;

  /// True if vertex within bounding box;
  bool IsBounded(const double *bbox);

  /// True if vertex within 2D bounding box;
  bool IsBounded2(const double *bbox);

  /// True if vertex is locked.
  bool IsLocked();

  /// Flag the vertex as being locked.
  void Lock();

  /// Set coordinate.
  void SetCoordinate(double x, double y, double z);

  /// Set coordinate.
  void SetCoordinate(double x, double y);

  /// Set coordinate.
  void SetCoordinate(const double *xyz, int dimension);

  void SetX(double x);
  void SetY(double y);
  void SetZ(double z);

  /// Set flag
  void SetFlag(unsigned flag);

  /// Set id
  void SetID(int id);

  /// Set the tolerance for floating point comparisons.
  static void SetTolerance(double tol);
 
  /// Flag the vertex as unlocked.
  void Unlock();

  /// Overloaded stream operator.
  friend std::ostream &operator<<(std::ostream& out, const Vertex& in);

  /// Overloaded assignment operator.
  Vertex &operator=(const Vertex& in);

 private:
  static int dimension;
  int id;
  double xyz[3];
  unsigned flag;
  bool lock;
};
#endif
