#!usr/bin/env python
# Benjamin Land - 15/10/14 <benland100@berkeley.edu>

import Common

def AnalyzeRootFiles(options):
    alphafile = 'BerkeleyAlphaBeta_alpha_' + str(Common.AlphaEnergy) + '.root'
    betafile = 'BerkeleyAlphaBeta_beta_' + str(Common.BetaEnergy) + '.root'
    
    alphapdf = Common.BinHitTimeResiduals(alphafile,options.timeFirst,options.timeLast,options.timeStep,options.retrigcutoff)
    betapdf = Common.BinHitTimeResiduals(betafile,options.timeFirst,options.timeLast,options.timeStep,options.retrigcutoff)
    
    ratdb  = '''
{
    name: "AB_PDF",
    index: "''' + options.index + '''",
    valid_begin: [0, 0],
    valid_end: [0, 0],
    retrig_cutoff: ''' + str(options.retrigcutoff) + ''',
    time_first: ''' + str(options.timeFirst) + ''',
    time_step: ''' + str(options.timeLast) + ''',
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
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "a50b5_center")
    parser.add_option("-f", type = 'float', dest = 'timeFirst', help = "First time in the time residual PDF.", default = -200.0)
    parser.add_option("-l", type = 'float', dest = 'timeLast', help = "Last time in the time residual PDF.", default = 1000.0)
    parser.add_option("-s", type = 'float', dest = 'timeStep', help = "Step time in the time residual PDF.", default = 1.0)
    parser.add_option("-r", type = 'float', dest = 'retrigcutoff', help = "Max retrigger wait time from start of previous event.", default = 600.0)
    (options, args) = parser.parse_args()
    AnalyzeRootFiles(options)
