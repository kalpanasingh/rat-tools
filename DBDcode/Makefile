#makefile compile author Nasim Fatemi-Ghomi
ROOT := ${ROOTSYS}
ROOTINC := ${ROOT}/include
ROOTLIB := ${ROOT}/lib
ROOTBIN := ${ROOT}/bin
#This needs to be changed to the direcotory where your code is
ANAINC:=/Users/nasim/analysis/analysiscode_dev/v_01
CXXFLAGS= -g -Wall -I$(ROOTINC) -I$(INCLUDE)
ROOTLIBS= -L$(ROOTLIB) $(shell $(ROOTBIN)/root-config --libs) 
ROOTGLIBS     = -L$(ROOTSYS)/lib $(shell $(ROOTSYS)/bin/root-config --glibs)
CXX :=g++

#list of object files
OBJS =DBDanalysis_mainTest.o DBDanalysisTest.o

# command to erase all files                                                    
RM              = /bin/rm -f


SRCS=DBDanalysis_mainTest.C src/DBDanalysisTest.cc

# program executable file name 
PROG =DBDanalysis_mainTest.exe

# top level rule, to compile everything 
all: $(PROG)

# rule for file "combinerootfile.o"                                                         
DBDanalysis_mainTest.o :DBDanalysis_mainTest.C
	@echo "<**Compiling**> "$<
	$(CXX) $(CXXFLAGS)  -I$(ROOTSYS)/include    -c DBDanalysis_mainTest.C -o  DBDanalysis_mainTest.o 

DBDanalysisTest.o :src/DBDanalysisTest.cc
	@echo "<**Compiling**> "$<
	$(CXX) $(CXXFLAGS)  -I$(ROOTSYS)/include    -c src/DBDanalysisTest.cc -o  DBDanalysisTest.o 

# rule to link the program                                                     
$(PROG) : $(OBJS)
	@echo "<**Linking**>"
	$(CXX) $(CXXFLAGS)  $(ROOTLIBS) $(ROOTGLIBS) -o $(PROG) $(OBJS)


clean:
	$(RM) $(PROG) $(OBJS)
