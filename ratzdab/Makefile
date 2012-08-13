CFLAGS = -Wno-write-strings -DSWAP_BYTES -g
INCLUDE = -Isrc -Iutil -Iutil/include -I$(ROOTSYS)/include -I$(RATROOT)/include -I$(RATROOT)/include/RAT
LFLAGS = -L$(ROOTSYS)/lib -L$(RATROOT)/lib

CC = g++
LIBS = -lrt -lCore -lRIO -lCint

ZCONVERT_SOURCES = src/zdab_convert.cpp util/PZdabFile.cxx util/SnoStr.cxx util/error_ph.c util/time_utils.cpp
ZFILE_SOURCES = src/zdab_file.cpp util/PZdabFile.cxx util/SnoStr.cxx util/error_ph.c util/time_utils.cpp
ZDISPATCH_SOURCES = src/zdab_dispatch.cpp
Z2R_SOURCES = src/zdab2root.cpp

all: libzfile libzconvert dispatch libratzdab zdab2root

zdab2root: libzfile libzconvert _zdab2root

dispatch: libconthost libzdispatch

examples: all _examples

libzconvert:
	$(CC) -shared -fPIC -o libzconvert.so $(ZCONVERT_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS)
	test -d lib || mkdir lib
	mv libzconvert.so lib

libzfile:
	$(CC) -shared -fPIC -o libzfile.so $(ZFILE_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS)
	test -d lib || mkdir lib
	mv libzfile.so lib

libconthost:
	test -d contrib/disp || (cd contrib && tar zxf disp.tar.gz && cd disp/src && patch -p0 < ../../disp_patch.diff)
	cd contrib/disp/src && make

libzdispatch:
	$(CC) -shared -fPIC -o libzdispatch.so $(ZDISPATCH_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) -Icontrib/disp/include -Lcontrib/disp/lib -lconthost
	test -d lib || mkdir lib
	mv libzdispatch.so lib

libratzdab:
	cd lib && ar rcs libratzdab.a libzconvert.so libzfile.so libzdispatch.so

_zdab2root:
	$(CC) -o zdab2root $(Z2R_SOURCES) $(INCLUDE) $(CFLAGS) $(CXXFLAGS) $(LFLAGS) $(LIBS) -Llib -lzfile -lzconvert -lRATEvent_Linux-g++ -lrat_Linux-g++
	test -d bin || mkdir bin
	mv zdab2root bin

_examples:
	cd examples && make

clean:
	if test -d contrib/disp; then cd contrib/disp/src && make clean; fi
	cd examples && make clean
	-$(RM) *.o lib/*.so lib/*.a bin/*

