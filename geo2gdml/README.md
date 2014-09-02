## geo2gdml
To use this tool Geant4 and ROOT must be installed with extra flags and xerces-c-3.1.1 must be installed.
The Geant4 cmake options are:

    -DXERCESC_ROOT_DIR=$XERCESCROOT
    -DGEANT4_USE_GDML=ON
    
The ROOT configure option is:

    --enable-gdml
    
By default snoing only adds the ROOT option.
