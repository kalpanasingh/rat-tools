g++ -Wall `root-config --cflags --glibs` -o Coordinate -Iinclude -I${ratLoc}/include -Iinclude/RAT -I${ratLoc}/include/RAT -I${ratLoc}/include/RAT/DS -L${ratLoc}/lib  -lRATEvent_Linux-g++ ${currentLoc}/Coordinate.cpp