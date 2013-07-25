def lotlat_deg_stereographic(longitude_deg, latitude_deg, central_longitude_deg=0.0, central_latitude_deg=-90.0, geoid_radious=6.37101e+06, central_point_buffer_deg=5.0):

##########################################################################
#  
#  Generation of boundary representation from arbitrary geophysical
#  fields and initialisation for anisotropic, unstructured meshing.
#  
#  Copyright (C) 2011-2013 Dr Adam S. Candy, adam.candy@imperial.ac.uk
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
##########################################################################

   '''Function converting lognitude and latitude into x & y coordinates on a stereographic
      projection plane tangent to the south pole.'''
   from scipy import pi, cos, sin
   #Convert longitude, latitude, central longitude and central latitude to radians.
   longitude_rad = longitude_deg*pi/180
   latitude_rad = latitude_deg*pi/180
   central_longitude_rad = central_longitude_deg*pi/180
   central_latitude_rad = central_latitude_deg*pi/180
   #Calculate coondinates in new projection.
   stereographic_x = ((2*geoid_radious)/(1 + sin(central_latitude_rad)*sin(latitude_rad) + cos(central_latitude_rad)*cos(latitude_rad)*cos(longitude_rad-central_longitude_rad)))*cos(latitude_rad)*sin(longitude_rad-central_longitude_rad)
   stereographic_y = ((2*geoid_radious)/(1 + sin(central_latitude_rad)*sin(latitude_rad) + cos(central_latitude_rad)*cos(latitude_rad)*cos(longitude_rad-central_longitude_rad)))*(cos(central_latitude_rad)*sin(latitude_rad) - sin(central_latitude_rad)*cos(latitude_rad)*cos(longitude_rad-central_longitude_rad))
   return stereographic_x, stereographic_y
