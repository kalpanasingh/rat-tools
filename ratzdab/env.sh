#!/bin/bash 
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
export LD_LIBRARY_PATH=$DIR/lib:$PWD/contrib/disp/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$DIR/lib:$PWD/contrib/disp/lib:$DYLD_LIBRARY_PATH
export RATZDAB_ROOT=$DIR
export PYTHONPATH=$DIR/python:$PYTHONPATH
export PATH=$DIR/bin:$PATH

