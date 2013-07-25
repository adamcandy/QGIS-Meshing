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

#include <algorithm>
#include <cassert>
#include <cmath>
#include <deque>
#include <iostream>
#include <map>
#include <set>
#include <vector>

#include <float.h>

#include "DecimateCoast.h"
#include "Ellipsoid.h"

using namespace std;

size_t DecimateCoast::ncalls=0;

DecimateCoast::DecimateCoast(){
  distance_to_edge=0.0;
  verbose=false;
  ncalls++;
}

double DecimateCoast::diagnostic(size_t v0, size_t v1, std::deque<Vertex>& coast) const{
  if(verbose)
    cout<<"double DecimateCoast::diagnostic("<<v0<<", "<<v1<<", std::deque<Vertex>&) const\n";
  
  double error = 0.0;
  size_t start=v0+1;
  if(v0>v1){
    for(size_t i=v0+1; i<coast.size(); i++){
      double r[3], r0[3], r1[3];
      coast[i].GetCoordinate(r);
      coast[v0].GetCoordinate(r0);
      coast[v1].GetCoordinate(r1);
      
      double d = get_d(r[0], r[1], r0[0], r0[1], r1[0], r1[1]);
      error = max(d, error);
    }
    start=0;
  }
  
  for(size_t i=start; i<v1; i++){
    double r[3], r0[3], r1[3];
    coast[i].GetCoordinate(r);
    coast[v0].GetCoordinate(r0);
    coast[v1].GetCoordinate(r1);
    double d = get_d(r[0], r[1], r0[0], r0[1], r1[0], r1[1]);
    
    error = max(d, error);
  }
  
  return error;
}

// Find the node that minimises the error on both edges.
size_t DecimateCoast::find_best(size_t v0, size_t v1, size_t v2, std::deque<Vertex>& coast) const{
  if(verbose)
    cout<<"size_t DecimateCoast::find_best(size_t v0, size_t v1, size_t v2, std::deque<Vertex>& coast) const\n";

  // Initialise
  pair<double, size_t> best(max(diagnostic(v1, v0, coast),
                                diagnostic(v0, v2, coast)), v0);
  
  size_t start=v1+1;
  if(v1>v0){
    for(size_t i=v1+1; i<coast.size(); i++){
      double r[3], r1[3], r2[3];
      coast[i].GetCoordinate(r);
      coast[v1].GetCoordinate(r1);
      coast[v2].GetCoordinate(r2);
      
      // Find worst case of the two
      double worst = max(diagnostic(v1, i,  coast),
                         diagnostic(i,  v2, coast));
      
      // Update best if the worst case is still better than the current
      // best
      if(worst<best.first)
        best = pair<double, size_t>(worst, i);
    }
    start = 0;
  }
  
  
  // -
  for(size_t i=start; i<v2; i++){
    double r[3], r1[3], r2[3];
    coast[i].GetCoordinate(r);
    coast[v1].GetCoordinate(r1);
    coast[v2].GetCoordinate(r2);
    
    // Find worst case of the two
    double worst = max(diagnostic(v1, i,  coast),
                       diagnostic(i,  v2, coast));
    
    // Update best if the worst case is still better than the current
    // best
    if(worst<best.first)
      best = pair<double, size_t>(worst, i);
  }
  
  return best.second;
}

// Find the next vertex along the shoreline
map< size_t, deque<size_t> >::iterator DecimateCoast::find_next(map< size_t, deque<size_t> >::iterator node,
                                                                map< size_t, deque<size_t> >& shoreline,
                                                                bool cyclic) const{
  node++;
  if((node==shoreline.end())&&cyclic)
    return shoreline.begin();
  return node;
}

map< size_t, deque<size_t> >::iterator DecimateCoast::find_prev(map< size_t, deque<size_t> >::iterator node,
                                                                map< size_t, deque<size_t> > &shoreline,
                                                                bool cyclic) const{
  if((node==shoreline.begin())&&(!cyclic))
    return shoreline.end();
  
  node--;
  if((node==shoreline.end())&&cyclic)
    return shoreline.find(shoreline.rbegin()->first);
  return node;
}

inline double DecimateCoast::get_d(double x,  double y,
                                   double x1, double y1,
                                   double x2, double y2) const{
  if(verbose)
    cout<<"double DecimateCoast::get_d("
        <<x <<", "<<y <<", "
        <<x1<<", "<<y1<<", "
        <<x2<<", "<<y2<<") const\n";
  
  double a2 = Ellipsoid::get_ds2(x, y, x1, y1);
  double a = sqrt(a2);
  
  double b2 = Ellipsoid::get_ds2(x, y, x2, y2);
  double b = sqrt(b2);
  
  double c2 = Ellipsoid::get_ds2(x1, y1, x2, y2);
  double c = sqrt(c2);

  // What is the base, c, is very small - => a~=b
  if((a+b)<1.0e-6*c)
    return a;
  
  // What if either a or b is very small - dist to edge ~=0
  if(fabs(a+b-c)<1.0e-6*c)
    return 0.0;

  double cosA = (b2 + c2 - a2)/(2*b*c);
  if(cosA<0.0){
    if(verbose)
      cout<<"error b = "<<b<<endl;
    return b;
  }

  double cosB = (a2 + c2 - b2)/(2*a*c);
  if(cosB<0.0){
    if(verbose)
      cout<<"error a = "<<a<<endl;
    return a;
  }
  
  double dist=0.0;
  if(cosA<1.0)
    dist = b*sin(acos(cosA));
  
  if(verbose)
    cout<<"error vert = "<<dist<<", "<<cosA<<endl;
  
  return dist;
}

double DecimateCoast::get_length(size_t v0, size_t v1, std::deque<Vertex>& coast) const{
  double r0[3], r1[3];
  coast[v0].GetCoordinate(r0);
  coast[v1].GetCoordinate(r1);
  
  return sqrt(Ellipsoid::get_ds2(r0[0], r0[1], r1[0], r1[1]));
}

double DecimateCoast::get_length(double x0, double y0, double x1, double y1) const{
  
  return sqrt(Ellipsoid::get_ds2(x0, y0, x1, y1));
}

double DecimateCoast::GetDistToEdge(double longitude, double latitude) const{
  // Can be generalised to be spatially varying.
  return distance_to_edge;
}

void DecimateCoast::Decimate(deque<Vertex> &coast, bool trim){
  if(verbose)
    cout<<"void DecimateCoast::Decimate(deque<Vertex> &coast, bool trim)\n";
  
  if(coast.empty())
    return;
  
  const bool island = !coast.begin()->IsLocked();
  
  if(island&&verbose)
    cout<<"closed loop\n";
  
  if(island)
    //coast.pop_back();
    coast.clear();

  return;

  // For each node on the coast (n0), the first element of the deque
  // container is the node to the left (n1) and the last is the vertex
  // to the right (n2). The nodes between the first and last enteries
  // in the deque are the nodes between these extream points - i.e. n0
  // and the decimated nodes.
  map< size_t, deque<size_t> > nodes;
  if(island){
    nodes[0].push_back(coast.size()-1);
    nodes[0].push_back(0);
    nodes[0].push_back(1);
  }
  for(size_t i=1;i<coast.size()-1;i++){
    nodes[i].push_back(i-1);
    nodes[i].push_back(i);
    nodes[i].push_back(i+1);
  }
  if(island){
    nodes[coast.size()-1].push_back(coast.size()-2);
    nodes[coast.size()-1].push_back(coast.size()-1);
    nodes[coast.size()-1].push_back(0);
  }
  if(island){
    assert(nodes.begin()->first==*nodes.rbegin()->second.rbegin());
  }

  // Sweep until there is nothing to do.
  bool enable_smoothening=false;
  for(int nsweep=0; nsweep<100; nsweep++){
    if(verbose)
      cout<<"Sweep "<<nsweep<<endl;
    
    // Clear and get out if this is a collapsed island.
    if(island&&(nodes.size()<3)){
      coast.clear();
      return;
    }
    
    size_t vary_cnt=0, rm_cnt=0;
    
    // Flag used to watch if coast is modified in a sweep.
    bool touched=false;
    
    deque<size_t> shuffle;
    for(map< size_t, deque<size_t> >::const_iterator it=nodes.begin(); it!=nodes.end();it++)
      shuffle.push_back(it->first);
    random_shuffle(shuffle.begin(), shuffle.end());
    
    for(deque<size_t>::const_iterator it=shuffle.begin();it!=shuffle.end(); it++){
	  
      map< size_t, deque<size_t> >::iterator node = nodes.find(*it);
      
      if(coast[node->first].IsLocked())
        continue;
      
      // Clear and get out if this is a collapsed island.
      if(island&&(nodes.size()<3)){
        coast.clear();
        return;
      }
      
      // Find the most useful node within this shoreline segment and
      // the error associated with that node.
      int n0 = *node->second.begin();
      int n1 = *node->second.rbegin();
      
      // Initialise the error
      double error = -1.0;
            
      if(error<0.0) // If it has not already been set
        error = diagnostic(n0, n1, coast);
      
      double r0[3], r1[3];
      coast[n0].GetCoordinate(r0);
      coast[n1].GetCoordinate(r1);
      
      double xmid = (r0[0]+r1[0])*0.5;
      double ymid = (r0[1]+r1[1])*0.5;
      
      if(verbose)
        cout<<"target "<<error<<" "<<GetDistToEdge(xmid, ymid)<<endl;
      
      if(error<=GetDistToEdge(xmid, ymid)){
        rm_cnt++;
        // Delete this node.
        if(verbose)
          cout<<"Removing node "<<node->first<<endl;
        touched = true;
		
        // Clear nodes and jump out now if we've just distroyed an island.
        if((nodes.size()<3)&&island){
          coast.clear();
          return;
        }
		
        // Fix next vertex.
        deque<size_t>::iterator loc = find(node->second.begin(), node->second.end(), node->first);
        assert(loc!=node->second.end());
		
        // Find the next vertex in the chain.
        map< size_t, deque<size_t> >::iterator next = find_next(node, nodes, island);
        if(next!=nodes.end()){
          if(verbose){
            cout<<"modify next vertex 3-: "<<next->first<<" :: ";
            for(deque<size_t>::iterator jt=next->second.begin();jt!=next->second.end();jt++)
              cout<<*jt<<", ";
            cout<<endl;
          }
          next->second.insert(next->second.begin(), node->second.begin(), loc);
          if(verbose){
            cout<<"modify next vertex 4-: "<<next->first<<" :: ";
            for(deque<size_t>::iterator jt=next->second.begin();jt!=next->second.end();jt++)
              cout<<*jt<<", ";
            cout<<endl;
          }
        }
		
        // fix previous vertex
        loc++;
        assert(loc!=node->second.end());
		
        // Find the previous vertex in the chain
        map< size_t, deque<size_t> >::iterator prev = find_prev(node, nodes, island);	
        if(prev!=nodes.end()){
          if(verbose){
            cout<<"modify previous vertex 1-: "<<prev->first<<" :: ";
            for(deque<size_t>::iterator jt=prev->second.begin();jt!=prev->second.end();jt++)
              cout<<*jt<<", ";
            cout<<endl;
          }
          prev->second.insert(prev->second.end(), loc, node->second.end());
          if(verbose){
            cout<<"modify previous vertex 2-: "<<prev->first<<" :: ";
            for(deque<size_t>::iterator jt=prev->second.begin();jt!=prev->second.end();jt++)
              cout<<*jt<<", ";
            cout<<endl;
          }
        }
		
        nodes.erase(node);
		
        //
        if( (prev!=nodes.end())&&(next!=nodes.end()) ){
          assert(*prev->second.rbegin()==next->first);
          assert(prev->first==*next->second.begin());
        }
		
        if(island)
          assert(nodes.begin()->first==*nodes.rbegin()->second.rbegin());
      }else if(enable_smoothening){
        // This is pretty expensive to lets delete stuff before tweaking
        size_t best=find_best(node->first, *node->second.begin(), *node->second.rbegin(), coast);
        if(best!=node->first){
          vary_cnt++;
          if(verbose){
            cout<<"shifting from "<<node->first<<" to "<<best<<", island="<<island<<endl<<"-o->";
            for(deque<size_t>::iterator nn = node->second.begin(); nn!=node->second.end(); nn++)
              cout<<*nn<<", ";
            cout<<endl;
          }
          assert(nodes.find(best)==nodes.end());
          touched=true;
		  
          map< size_t, deque<size_t> >::iterator prev = find_prev(node, nodes, island);
          if(verbose){
            if(prev!=nodes.end())
              cout<<"prev = "<<prev->first<<endl;
            else
              cout<<"prev = null"<<endl;
          }
		  
          map< size_t, deque<size_t> >::iterator next = find_next(node, nodes, island);
          if(verbose){
            if(next!=nodes.end())
              cout<<"next = "<<next->first<<endl;
            else
              cout<<"next = null"<<endl;
          }
		  
          nodes[best].swap(node->second);
          nodes.erase(node);
		  
          if(verbose){
            cout<<"middle CCC: "<<best<<" :: ";
            for(deque<size_t>::iterator jt=nodes[best].begin();jt!=nodes[best].end();jt++)
              cout<<*jt<<", ";
            cout<<endl;
          }
		  
          if(prev!=nodes.end()){ // fix prev
            if(verbose){
              cout<<"modify previous CCC: "<<prev->first<<" :: ";
              for(deque<size_t>::iterator jt=prev->second.begin();jt!=prev->second.end();jt++)
                cout<<*jt<<", ";
              cout<<endl;
            }
			
            deque<size_t>::iterator ploc = find(prev->second.begin(), prev->second.end(), (size_t)best);
            if(ploc==prev->second.end()){
              deque<size_t>::iterator loc0 = find(nodes[best].begin(), nodes[best].end(), *prev->second.rbegin());
              loc0++;
              deque<size_t>::iterator loc1 = find(nodes[best].begin(), nodes[best].end(), (size_t)best);
              loc1++;
			  
              prev->second.insert(prev->second.end(), loc0, loc1);
            }else{
              ploc++;
              assert(find(prev->second.begin(), prev->second.end(), *ploc)!=prev->second.end());
              prev->second.erase(ploc, prev->second.end());
            }
			
            if(verbose){
              cout<<"modify previous CCC: "<<best<<" :: ";
              for(deque<size_t>::iterator jt=prev->second.begin();jt!=prev->second.end();jt++)
                cout<<*jt<<", ";
              cout<<endl;
            }
          }
		  
          if(next!=nodes.end()){ // fix next
            if(verbose){
              cout<<"modify next CCC: "<<best<<" :: ";
              for(deque<size_t>::iterator jt=next->second.begin();jt!=next->second.end();jt++)
                cout<<*jt<<", ";
              cout<<endl;
            }
			
            deque<size_t>::iterator nloc = find(next->second.begin(), next->second.end(), (size_t)best);
            if(nloc==next->second.end()){
              deque<size_t>::iterator loc0 = find(nodes[best].begin(), nodes[best].end(), (size_t)best);
              deque<size_t>::iterator loc1 = find(nodes[best].begin(), nodes[best].end(), *next->second.begin());
              next->second.insert(next->second.begin(), loc0, loc1);
            }else{
              next->second.erase(next->second.begin(), nloc);
            }
			
            if(verbose){
              cout<<"modify next CCC: "<<best<<" :: ";
              for(deque<size_t>::iterator jt=next->second.begin();jt!=next->second.end();jt++)
                cout<<*jt<<", ";
              cout<<endl;
            }
          }
        }
      }
    }
    if(verbose)
      cout<<"sweep "<<nsweep<<", removed "<<rm_cnt<<", varied "<<vary_cnt<<endl;
    
    if(((!touched)||(nodes.empty()))&&(nsweep!=0)&&enable_smoothening)
      break;
    
    //if((rm_cnt==0)||(nsweep==1))
    //  enable_smoothening=true;
  }
  
  if(trim&&(nodes.size()<3)){
    nodes.clear();
    coast.clear();
  }else{
    if(island){
      assert(nodes.begin()->first==*nodes.rbegin()->second.rbegin());
    }else{
      assert(*nodes.begin()->second.begin()==0);
      assert(*nodes.rbegin()->second.rbegin()==(coast.size()-1));
    }
    deque<Vertex> new_coast;
    if(coast.begin()->IsLocked())
      new_coast.push_back(*coast.begin());
    for(map< size_t, deque<size_t> >::iterator jt=nodes.begin();jt!=nodes.end();jt++)
      new_coast.push_back(coast[jt->first]);
    if(coast.rbegin()->IsLocked())
      new_coast.push_back(*coast.rbegin());
    else
      new_coast.push_back(*new_coast.begin());

    coast.swap(new_coast);
  }
  
  if(verbose)
    cout<<"Finished decimation. "<<coast.size()<<" nodes left\n";
  return;
}

void DecimateCoast::SetError(double error){
  if(verbose)
    cout<<"void DecimateCoast::SetError("<<error<<")"<<endl;
  distance_to_edge = error;
}

void DecimateCoast::SphericalProjectionOn(){}

void DecimateCoast::StereographicProjectionOn(){
  cerr<<"ERROR: no longer supported - "<<__FILE__<<", "<<__LINE__<<endl;
  exit(-1);
}

void DecimateCoast::VerboseOn(){
  verbose=true;
}
