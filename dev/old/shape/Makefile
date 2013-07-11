CC      = gcc
CFLAGS  = -Wall

.SUFFIXES: .c .o

.PHONY: all clean

all : run


run: produceGeo.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f *.o
	rm -f run 
