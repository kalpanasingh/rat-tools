#!usr/bin/env python
# Benjamin Land - 15/10/14 <benland100@berkeley.edu>

import Utilities, os

def AnalyzeRootFiles(options):
    alphafile = 'BerkeleyAlphaBeta_alpha_' + str(Utilities.AlphaEnergy) + '.root'
    betafile = 'BerkeleyAlphaBeta_beta_' + str(Utilities.BetaEnergy) + '.root'
    
    launch = 'python -c \'import AnalyseData; AnalyseData.AnalysisFunction('+ \
        '"'+alphafile+'",' + \
        '"'+betafile+'",' + \
        '"'+options.index+'",' + \
        str(options.timeFirst)+',' + \
        str(options.timeLast)+',' + \
        str(options.timeStep)+',' + \
        str(options.retrigcutoff)+')\''
    
    #run analysis as batch or regular execution
    if options.batch:
        batch_params = {}
        execfile(options.batch, {}, batch_params)
    
        inFile = open("Template_Batch.sh", "r")
        rawText = string.Template(inFile.read())
        inFile.close()
        
        outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                     Ratenv = batch_params['ratenv'],
                                     Cwd = os.environ['PWD'].replace("/.", "/"),
                                     RunCommand = launch)
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()
		
        os.system(batch_params["submit"] + " AnalyseData.sh")				
    else:
        os.system(launch)

def AnalysisFunction(alphafile,betafile,index,timeFirst,timeLast,timeStep,retrigcutoff):
    alphapdf = Utilities.BinHitTimeResiduals(alphafile,timeFirst,timeLast,timeStep,retrigcutoff)
    betapdf = Utilities.BinHitTimeResiduals(betafile,timeFirst,timeLast,timeStep,retrigcutoff)
    
    ratdb  = '''
{
    name: "AB_PDF",
    index: "''' + index + '''",
    run_range: [0, 0],
    pass : 0,
    production: false,
    comment: \"\",
    retrig_cutoff: ''' + str(retrigcutoff) + ''',
    time_first: ''' + str(timeFirst) + ''',
    time_step: ''' + str(timeLast) + ''',
    scale_factor: 1.0,
    pdf_alpha_prob: [''' + ','.join(['%0.14e' % val for val in alphapdf]) + ''']
    pdf_beta_prob: [''' + ','.join(['%0.14e' % val for val in betapdf]) + '''] 
}
    '''
    
    outfile = open('CLASSIFIER_BERKELEY_AB.ratdb','w')
    outfile.write(ratdb)
    outfile.close()
    
    print('CLASSIFIER_BERKELEY_AB.ratdb successfully written.\nAdd/replace the contents to rat/data/CLASSIFIER_BERKELEY_AB.ratdb as needed')

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option('-b', type='string', dest='batch', help='Run in batch mode' )
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result. (empty as default)", default = "")
    parser.add_option("-f", type = 'float', dest = 'timeFirst', help = "First time (in ns) in the time residual PDF (200)", default = -200.0)
    parser.add_option("-l", type = 'float', dest = 'timeLast', help = "Last time (in ns) in the time residual PDF (1000)", default = 1000.0)
    parser.add_option("-s", type = 'float', dest = 'timeStep', help = "Step time (in ns) in the time residual PDF (1)", default = 1.0)
    parser.add_option("-r", type = 'float', dest = 'retrigcutoff', help = "Max retrigger wait time (in ns) from start of previous event (600)", default = 600.0)
    (options, args) = parser.parse_args()
    AnalyzeRootFiles(options)
