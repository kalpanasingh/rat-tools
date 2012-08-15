CFLAGS = -Wno-write-strings -DSWAP_BYTES -g -fdiagnostics-show-option
INCLUDE = -Isrc -Iutil -Iutil/include -I$(ROOTSYS)/include -I$(RATROOT)/include -I$(RATROOT)/include/RAT
LFLAGS = -Llib -L$(ROOTSYS)/lib -L$(RATROOT)/lib

CC = g++
LIBS = -lrt -lCore -lRIO -lCint

ZCONVERT_SOURCES = src/zdab_convert.cpp util/PZdabFile.cxx
ZFILE_SOURCES = src/zdab_file.cpp util/PZdabFile.cxx
ZDISPATCH_SOURCES = src/zdab_dispatch.cpp
Z2R_SOURCES = src/zdab2root.cpp

all: libzconvert libzfile libzdispatch libratzdab.a zdab2root

libzconvert: libzconvert.so

libzfile: libzconvert libzfile.so

libzdispatch: libconthost libzconvert libzdispatch.so

zdab2root: libzfile _zdab2root

examples: all _examples

libzconvert.so:
	$(CC) -shared -fPIC -o libzconvert.so $(ZCONVERT_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) -lRATEvent_Linux-g++ -lrat_Linux-g++
	test -d lib || mkdir lib
	mv libzconvert.so lib

libzfile.so:
	$(CC) -shared -fPIC -o libzfile.so $(ZFILE_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) -lzconvert
	test -d lib || mkdir lib
	mv libzfile.so lib

libconthost:
	test -d contrib/disp || (cd contrib && tar zxf disp.tar.gz && cd disp/src && patch -p0 < ../../disp_patch.diff)
	cd contrib/disp/src && make

libzdispatch.so:
	$(CC) -shared -fPIC -o libzdispatch.so $(ZDISPATCH_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) -Icontrib/disp/include -Lcontrib/disp/lib -lconthost -lzconvert
	test -d lib || mkdir lib
	mv libzdispatch.so lib

libratzdab.a:
	cd lib && ar rcs libratzdab.a libzconvert.so libzfile.so libzdispatch.so

_zdab2root:
	$(CC) -o zdab2root $(Z2R_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) -Llib -lzfile -lzconvert
	test -d bin || mkdir bin
	mv zdab2root bin

_examples:
	cd examples && make

clean:
	if test -d contrib/disp; then cd contrib/disp/src && make clean; fi
	cd examples && make clean
	-$(RM) *.o lib/*.so lib/*.a bin/*

