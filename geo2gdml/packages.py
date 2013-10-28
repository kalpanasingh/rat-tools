import os

# Appends Xerces-C++
def xercesc(env):
    if "XERCESCROOT" in os.environ:
        env.Append( CPPPATH = [ os.environ["XERCESCROOT"] + "/include" ] )
        env.Append( LIBPATH = [ os.environ["XERCESCROOT"] + "/lib" ] )
    env.Append( LIBS = ['xerces-c'] )

# Appends Geant4 and CLHEP
def geant4(env):
    env.ParseConfig( "geant4-config --cflags --libs" )
    env.ParseConfig( "clhep-config --include --libs" )

# Appends ROOT
def root(env):
    ROOTSYS = os.path.join(os.environ["ROOTSYS"], 'bin')
    env.ParseConfig( os.path.join(ROOTSYS, 'root-config') + " --cflags --ldflags --libs ")
    env.Append( CPPPATH = [ os.environ["ROOTSYS"] + "/include"])
    env.Append( LIBS = 'PyROOT' )

# Appends RAT
def rat(env):
    env.Append( CPPPATH = [ os.environ["RATROOT"] + "/include" ] )
    env.Append( LIBPATH = [ os.environ["RATROOT"] + "/lib" ] )
    env.Append( LIBS = [ 'RATEvent_' + os.environ["RATSYSTEM"], 'rat_' + os.environ["RATSYSTEM"] ] )
    Curl(env)

# Appends Curl and Bzip (for RAT)
def Curl(env):
    env.Append( LIBS = [ "bz2" ] )
    if "BZIPROOT" in os.environ:
        env['CPPPATH'].append( os.environ['BZIPROOT'] + "/include" )
        env['LIBPATH'].append( os.environ['BZIPROOT'] + "/lib" )
    env.ParseConfig( "curl-config --cflags --libs" )

# Adds all packages
def addpackages(env):
    rat(env)
    geant4(env)
    root(env)
    xercesc(env)


