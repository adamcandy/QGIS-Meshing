#include <stdio.h>
#include <string.h>
#include <stlib.h>

#define VAL 10
#define SUCCESS 1
#define MATH_EVAL_LINE 38
#define BUFFER_SIZE 300

int showMesh(void) {
	int i = system("gmsh -2 box.geo");
	if (i==-1)
		return i;
	system("gmsh box.msh");
	return SUCCESS
}

void changeMathEval(int new) {
	FILE *read;
  read = fopen("box.geo","r");
	FILE *write;
	write = fopen("temp.geo","w");
	if (write==NULL) {
	  perror("ERROR in opening file to write\n");
    exit(EXIT_FAILURE);
	}
  char *buffer = (char *) malloc(BUFFER_SIZE * sizeof(char));
  if (read==NULL) {
    perror("ERROR in opening file\n");
    exit(EXIT_FAILURE);
  }
	int i = 1;
  while (!feof(read)){
    memset(buffer, 0, ((sizeof(char))*BUFFER_SIZE));
    fgets (buffer, BUFFER_SIZE, read); 
		if (i==MATH_EVAL_LINE) {
			char *temp = calloc(BUFFER_SIZE);
			temp = strncpy(temp,buffer,strlen(buffer)-5);
			char *num = calloc((new/10) + 2);
			temp = strcpy(temp,itoa(new,num,10));
			fputs(temp,write);
			fputs(";\n",write);
			free(temp);
			free(num);
		} else {
			fputs(buffer,write);
		}
		i++;
  }
  free(buffer);
	free(read);
	free(write);
  fclose(read);
}

int main(void) {
	for ( int i = 0; i< ; i+=15) {
		changeMathEval(i);
		showMesh();

	}
}
