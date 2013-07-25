
//////////////////////////////////////////////////////////////////////////
//  
//  QGIS-meshing plugins.
//  
//  Copyright (C) 2012-2013 Imperial College London and others.
//  
//  Please see the AUTHORS file in the main source directory for a
//  full list of copyright holders.
//  
//  Dr Adam S. Candy, adam.candy@imperial.ac.uk
//  Applied Modelling and Computation Group
//  Department of Earth Science and Engineering
//  Imperial College London
//  
//  This library is free software; you can redistribute it and/or
//  modify it under the terms of the GNU Lesser General Public
//  License as published by the Free Software Foundation,
//  version 2.1 of the License.
//  
//  This library is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  Lesser General Public License for more details.
//  
//  You should have received a copy of the GNU Lesser General Public
//  License along with this library; if not, write to the Free Software
//  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
//  USA
//  
//////////////////////////////////////////////////////////////////////////

//this file is for testing of the extraction of the points from
//GSSHS shape file

#include <stdlib.h>
#include <stdio.h>

int main(void) {
	/*
	assert(argc==4 && "Incorrect number of arguments passed" );
	char read[] = argv[1];
	char bound[] = argv[2];
	char write[] = argv[3];

	char *command1 = malloc(COMMAND_SIZE);
	if (command1==NULL) {
		printf("MALLOC FAILURE");
		exit(SYSTEM_FAILURE);
		return(EXIT_FAILURE);
	}
	*/
	char command1[] = "python makeShapefile.py; rm test.* ; rm m.txt ; python extractPoints.py GSHHS_c_L1.shp polygon.shp test 5 > m.txt ; cat m.txt";
	char command2[] = "rm shpTest.geo; python makeGeoFile.py test.shp shpTest";
	char command3[] = "gmsh -2 shpTest.geo>t.txt ; rm t.txt";
	char command4[] = "gmsh shpTest.msh";
	system(command1);
	system(command2);
	printf("Meshing...\n");
	system(command3);
	printf("done...\n");
	system(command4);
	return 1;
}
