CFLAGS = -Wno-write-strings -DSWAP_BYTES -g -fdiagnostics-show-option
INCLUDE = -Isrc -Iutil -Iutil/include -I$(ROOTSYS)/include -I$(RATROOT)/include -I$(RATROOT)/include/RAT
LFLAGS = -Llib -L$(ROOTSYS)/lib -L$(RATROOT)/lib

CC = g++
LIBS = $(shell root-config --libs)
RAT_LIBS = -lRATEvent_$(shell uname)

ZCONVERT_SOURCES = src/zdab_convert.cpp util/PZdabFile.cxx
ZFILE_SOURCES = src/zdab_file.cpp util/PZdabFile.cxx
ZDISPATCH_SOURCES = src/zdab_dispatch.cpp
Z2R_SOURCES = src/zdab2root.cpp

RAT_INC = $(RATROOT)/include/RAT
DICT_SOURCES = src/zdab_dispatch.hpp src/zdab_file.hpp src/zdab_convert.hpp $(RAT_INC)/DS/Digitiser.hh $(RAT_INC)/DS/PMTUnCal.hh $(RAT_INC)/Extensible.hh util/include/Record_Info.h src/linkdef.h


all: libzconvert.so libzfile.so libconthost libzdispatch.so libratzdab.a zdab2root rootlib

libzconvert: libzconvert.so lib

libzfile: libzconvert.so libzfile.so lib

libzdispatch: libconthost libzconvert.so libzdispatch.so lib

zdab2root: lib libzconvert.so libzfile.so _zdab2root

examples: all _examples

lib:
	test -d lib || mkdir lib

rootlib:
	test -d build || mkdir build
	$(ROOTSYS)/bin/rootcint -f ./build/ratzdab_dict.cxx -c -p -Isrc $(INCLUDE) $(DICT_SOURCES)
	$(CC) -o lib/ratzdab_root.so -shared -fPIC $(CFLAGS) build/ratzdab_dict.cxx src/zdab_convert.cpp src/zdab_file.cpp src/zdab_dispatch.cpp util/PZdabFile.cxx -I. -Icontrib/disp/include $(INCLUDE) -Lcontrib/disp/lib $(LFLAGS) $(RAT_LIBS) $(LIBS) -lconthost

libzconvert.so:
	$(CC) -shared -fPIC -o libzconvert.so $(ZCONVERT_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(RAT_LIBS) $(LIBS)
	test -d lib || mkdir lib
	mv libzconvert.so lib

libzfile.so:
	$(CC) -shared -fPIC -o libzfile.so $(ZFILE_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) -lzconvert $(LIBS)
	test -d lib || mkdir lib
	mv libzfile.so lib

libconthost:
	test -d contrib/disp || (cd contrib && tar zxf disp.tar.gz && cd disp && patch -p0 < ../disp_patch.diff && cd src && make clean)
	cd contrib/disp/src && make

libzdispatch.so:
	$(CC) -shared -fPIC -o libzdispatch.so $(ZDISPATCH_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) -Icontrib/disp/include -Lcontrib/disp/lib -lconthost -lzconvert
	test -d lib || mkdir lib
	mv libzdispatch.so lib

libratzdab.a:
	cd lib && ar rcs libratzdab.a libzconvert.so libzfile.so libzdispatch.so

_zdab2root:
	$(CC) $(CFLAGS) -o zdab2root $(Z2R_SOURCES) $(INCLUDE) $(CXXFLAGS) $(LFLAGS) -Llib -lzfile -lzconvert $(RAT_LIBS) $(LIBS)
	test -d bin || mkdir bin
	mv zdab2root bin

_examples:
	cd examples && make

clean:
	if test -d contrib/disp; then cd contrib/disp/src && make clean; fi
	cd examples && make clean
	-$(RM) *.o lib/*.so lib/*.a bin/* python/*.pyc
	-$(RM) -rf build *.dSYM lib/*.dSYM

