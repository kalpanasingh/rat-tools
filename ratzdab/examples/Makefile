CFLAGS = -g
INCLUDE = -I../src -I$(ROOTSYS)/include -I$(RATROOT)/include
LFLAGS = -L../lib -L$(RATROOT)/lib
LIBS = -lratzdab

ROOT = -I$(ROOTSYS)/include -L$(ROOTSYS)/lib -lCore -lRIO -lCint
RAT = -I$(RATROOT)/include -L$(RATROOT)/lib -lRATEvent_Linux-g++ -lrat_Linux-g++

CC = g++

all: print_dispatch

print_dispatch:
	$(CC) -o print_dispatch print_dispatch.cpp $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) $(ROOT) $(RAT)

clean:
	-$(RM) *.o print_dispatch

