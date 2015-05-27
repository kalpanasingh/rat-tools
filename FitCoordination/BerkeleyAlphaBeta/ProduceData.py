#!/usr/bin/env python
# Benjamin Land - 15/10/14 <benland100@berkeley.edu>

import os, sys, string, Utilities

def ProduceData(options):
    '''Generates macros to generate the root files containing events to be processed.'''
    
    #load the template for the macros
    macroin = open('Template_Macro.mac', 'r')
    basemacro = string.Template(macroin.read())
    macroin.close()

    extraDB = ('/rat/db/load ' + options.loadDB) if options.loadDB else ''
 
    #generate the alpha macro
    alphafile = 'BerkeleyAlphaBeta_'+options.scintMaterial+'_alpha_' + str(Utilities.AlphaEnergy)
    for batch in range(0,Utilities.Batches):
     alphaout = open(alphafile+'_'+str(batch)+'.mac', 'w')
     alphaout.write(basemacro.substitute(Generator = '/generator/vtx/set alpha 0 0 0 ' + str(Utilities.AlphaEnergy),
                                         OutFileName = alphafile + '_' + str(batch) + '.root',
                                         GeoFile = options.geoFile,
                                         ScintMaterial = options.scintMaterial,
                                         ExtraDB = extraDB,
                                         NEvents = str(int(Utilities.TotalEvents/Utilities.Batches))))
     alphaout.close()

    #generate the beta macro
    betafile = 'BerkeleyAlphaBeta_'+options.scintMaterial+'_beta_' + str(Utilities.BetaEnergy)
    for batch in range(0,Utilities.Batches):
     betaout = open(betafile+'_'+str(batch)+'.mac', 'w')
     betaout.write(basemacro.substitute( Generator = '/generator/vtx/set e- 0 0 0 ' + str(Utilities.BetaEnergy),
                                         OutFileName = betafile + '_'+str(batch)+'.root',
                                         GeoFile = options.geoFile,
                                         ScintMaterial = options.scintMaterial,
                                         ExtraDB = extraDB,
                                         NEvents = str(int(Utilities.TotalEvents/Utilities.Batches))))
     betaout.close()
    
    #list-o-macros
    macros = [ alphafile, betafile ]
    
    #check for batch options
    if options.batch:
        batch_params = {}
        execfile( options.batch, {}, batch_params )
        batchin = open('Template_Batch.sh', 'r' )
        basebatch = string.Template( batchin.read() )
        batchin.close()
    
    #run the macros
    for macro in macros:
        for batch in range(0,Utilities.Batches):
         launch = 'rat ' + macro + '_' + str(batch) + '.mac -l ' + macro + '_'+str(batch)+'.log'
         if options.batch:
             batch = basebatch.substitute( Preamble = '\n'.join(s for s in batch_params['preamble']),
                                           Cwd = os.environ['PWD'].replace('/.', '/'),
                                           RunCommand = launch,
                                           Ratenv = batch_params['ratenv'] )
             batchout = open(macro + '.sh', 'w')
             batchout.write(batch)
             batchout.close()
             os.system(batch_params['submit'] + ' ' + macro +'.sh' )
         else:
             os.system(launch)


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = 'usage: %prog [options] target', version = '%prog 1.0')
    parser.add_option('-g', type = 'string', dest = 'geoFile', help = 'Geometry File to use (geo/snoplus.geo).', default = 'geo/snoplus_simple.geo') #switch to simple until snoplus.geo is fixed
    parser.add_option('-s', type = 'string', dest = 'scintMaterial', help = 'Scintillator material (labppo_scintillator)', default = 'labppo_scintillator')
    parser.add_option('-p', type = 'string', dest = 'particle', help = 'Particle type (ignored for this coordinator)', default = '')
    parser.add_option('-b', type='string', dest='batch', help='Run in batch mode' )
    parser.add_option('-l', type='string', dest='loadDB', help='Load an extra DB directory')
    (options, args) = parser.parse_args()
    ProduceData(options)
    
