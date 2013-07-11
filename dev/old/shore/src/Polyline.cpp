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

#include <cstdio>
#include <cstdlib>

#include <vtkPolyData.h>
#include <vtkCellData.h>
#include <vtkPointData.h>
#include <vtkXMLPolyDataWriter.h>
#include <vtkZLibDataCompressor.h>

#include <fstream>
#include <sstream>
#include <vector>

#include "Polyline.h"
#include "DecimateCoast.h"

using namespace std;

bool Polyline::verbose=false;

int Polyline::GetNumberOfPolys(){
  return polylines.size();
}

void Polyline::Simplify(double distance_to_edge){
  if(verbose)
    cout<<"Polyline::Simplify(...)\n";
  
  for(size_t i=0;i<polylines.size();i++){
    DecimateCoast filter;

    if(verbose)
      filter.VerboseOn();

    filter.SetError(distance_to_edge);

    if(verbose){
      cout<<"before: "<<polylines[i].size()<<endl;
    }
    
    filter.Decimate(polylines[i]);
  }
}

void Polyline::ReadGMT(string filename){
  if(verbose)
    cout<<"void Polyline::ReadGMT(string filename)\n";

  // Check that the file exists.
  fstream afile;
  afile.open(filename.c_str(), ios::in);
  if(!afile.is_open()){
    cerr<<"ERROR: Polyline data file, "<<filename
        <<", cannot be opened. Does it exist? Have you read permission?\n";
    exit(-1);
  }
  afile.close();
  
  FILE *shorefile=fopen(filename.c_str(), "r");
  char buffer[1024];
  string start, finish;
  int id=0;
  for(;;){
    deque<Vertex> polyline;
    char *s=NULL;
    for(;;){
      s = fgets(buffer, 1024, shorefile);
      if(s==NULL)
	break;
      
      if(!isdigit(s[0])){
	if(s[0]=='-'){ 
	  if(!isdigit(s[1])){
	    break; 
	  }
	}else{
	  break;
	}
      }

      if(start.empty())
        start = s;
      else
        finish = s;

      double longitude, latitude;
      int rcnt = sscanf(buffer, "%lf %lf", &longitude, &latitude);
      if(rcnt<2){
        cerr<<"ERROR: foobar read of longitude and latitude.\n";
        exit(-1);
      }
      polyline.push_back(Vertex(id++, longitude, latitude));
    }

    if(!polyline.empty()){
      //      if(start!=finish){
      polyline.begin()->Lock();
      polyline.rbegin()->Lock();
      //      }
    }

    if(!polyline.empty()){
      polylines.push_back(polyline);
    }
    
    if(s==NULL) 
      break;
  }
  
  fclose(shorefile);
  return;
}

void Polyline::WriteVTK(string basename){
  if(verbose)
    cout<<"void Polyline::WriteVTK(string basename)\n";
  string filename(basename+".vtp");

  // Write out VTK polydata file.
  vtkPolyData *dataSet = vtkPolyData::New();
  dataSet->Allocate();
  vtkPoints *Pts = vtkPoints::New();
  Pts->SetDataTypeToDouble();
  for(size_t i=0;i<polylines.size();i++){
    if(!polylines[i].empty()){
      
      for(size_t j=0;j<polylines[i].size();j++){
        double x, y, z;
	polylines[i][j].GetCoordinate(x, y, z);
	Pts->InsertNextPoint(x, y, z);
      }
    }
  }
  dataSet->SetPoints(Pts); 
  Pts->Delete();

  vtkIdType cnt=0;
  for(size_t i=0;i<polylines.size();i++){ 
    if(polylines[i].size()){
      std::vector<vtkIdType> cell;
      for(size_t j=0;j<polylines[i].size();j++)
        cell.push_back(cnt++);
      dataSet->InsertNextCell(VTK_POLY_LINE, cell.size(), &(cell[0]));
    }
  }
  
  vtkIntArray *ids = vtkIntArray::New();
  ids->SetNumberOfTuples(polylines.size());
  ids->SetNumberOfComponents(1);
  ids->SetName("segment");
  for(size_t i=0;i<polylines.size();i++){
    ids->SetTuple1(i, i);
  }
  dataSet->GetCellData()->AddArray(ids);
  dataSet->Update();
  ids->Delete();


  vtkXMLPolyDataWriter *writer= vtkXMLPolyDataWriter::New();
  vtkZLibDataCompressor* compressor = vtkZLibDataCompressor::New();
  writer->SetFileName(filename.c_str());
  writer->SetInput(dataSet);
  writer->SetCompressor(compressor);
  writer->Write();
  writer->Delete();
  dataSet->Delete();
  compressor->Delete();

  return;
}

void Polyline::WriteGMT(string basename){
  if(verbose)
    cout<<"void Polyline::WriteGMT(string basename)\n";
  
  // Open file for writing.
  string filename(basename+".gmt");
  ofstream file;
  file.open(filename.c_str());
  file.precision(16);
  
  // Write out polygons/lines file.
  int npolylines=0;
  for(size_t i=0;i<polylines.size();i++){
    if(polylines[i].size()<2)
      continue;
    npolylines++;
    file<<"> "<<npolylines<<endl;
    for(size_t j=0;j<polylines[i].size();j++){
      double x, y, z;
      polylines[i][j].GetCoordinate(x, y, z);
      file<<x<<" "<<y<<" "<<z<<endl;
    }
  }
  
  file.close();
  return;
}

void Polyline::VerboseOn(){
  verbose = true;
}

void Polyline::VerboseOff(){
  verbose = false;
}
