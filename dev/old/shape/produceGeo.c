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
