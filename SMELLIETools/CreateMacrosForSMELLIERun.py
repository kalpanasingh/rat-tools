#IMPORTANT:you may need to download the couchdb python module from https://github.com/djc/couchdb-python.
import couchdb
import sys

# TODO: fix up intensity -> Nphotons mapping !!!!

#EXAMPLE: an example command line argument for this program $python runInfoSmellie.py 9044

# In this example, you will access the SMELLIE run info for run 9044, and extract the information for each subrun and create a
# rat macro for it

#check to see if the runNumber has been given as an argument
if(len(sys.argv) < 2):
    exit("Exit:Please run in terminal as '$python runInfoSmellie.py <runNumber>'")
    
runNumber = int(sys.argv[1])

#connect to the SNO+ database
db = couchdb.Server("http://snoplus:PureTe->Dirac!=True@couch.snopl.us")

#fetch the SMELLIE DB from within the main SNO+ Database
smellieDb = db['smellie']

#Python dictionary to fill with information for a given run
infoForRun = dict()

#Python dictionary to fill with informatin for a given subrun
infoForSubRun = dict()

#Python dictionary to fill with the run description information
runDescriptionInfo = dict()

#BOOL to see if the run is a SMELLIE run, this checks to see if the run number given actually is a smellie run
isRunASmellieRun = False

#loop through all the results and find the runNumber, this is dependent upon the view being present online
for row in smellieDb.view('_design/runNumbers/_view/runNumbers'):
    
    if(row.key == runNumber):
        runDocId = row.value['_id']
        isRunASmellieRun = True
        infoForRun = row.value

if (isRunASmellieRun == False):
    print "\nRun " + str(runNumber) + " is not a valid SMELLIE run or database data is not present for this run\n"
    exit()

print "Fetching associated run description document for run :" + str(runNumber) + "\n"

#loop through a different view to pick out the relevant runNumber information - seems we have to do this afterwards?
#NOTE:this is dependent upon a view that exists on couchdb, if the view is deleted, this will not work
for row in smellieDb.view('_design/smellieMainQuery/_view/pullEllieRunHeaders'):
    
    if(row.value['run_name'] == infoForRun['run_description_used']):
        runDescriptionInfo = row.value
        for keyField in runDescriptionInfo:
            if(keyField == 'trigger_frequency'):
                simfrequency = runDescriptionInfo[keyField]
            if(keyField == 'triggers_per_loop'):
                simstats = runDescriptionInfo[keyField]
            print "RunLevelInfoFromDescription:\t" + str(keyField) + ":\t" + str(runDescriptionInfo[keyField])

print "\n"

max_subrun = 0
#loop through all the results and find the runNumber again (which we know exists), this time extract the subrun info we need
for row in smellieDb.view('_design/runNumbers/_view/runNumbers'):    
    
    if(row.key == runNumber):
        runDocId = row.value['_id']
        isRunASmellieRun = True
        # Now loop through subruns till they run out
        subRunNumber = 0
        exists = 1
        while exists!=0:
            subRunNumber+=1
            print "Fetching information for run :" + str(runNumber) + " sub_run :" + str(subRunNumber) + "\n"
            infoForRun = row.value
            for keyField in infoForRun:
                if(keyField == 'sub_run_info'):
                    try:
                        infoForSubRun['fibre'] = infoForRun[keyField][subRunNumber-1]['fibre']
                        infoForSubRun['intensity'] = infoForRun[keyField][subRunNumber-1]['intensity']
                        infoForSubRun['laser'] = infoForRun[keyField][subRunNumber-1]['laser']
                        #manipulate the laser name to remove the 'nm'
                        string =str(infoForSubRun['laser'])[0:3]
                        infoForSubRun['laserWL'] = string
                        #manipulate the intensity - need algorithm to convert from 0-100 to number of photons
                        #as a placeholder - multiply by a factor
                        Nphotons = 2000+10*int(infoForSubRun['intensity'])
                        #Now we have all the info to write the macro
                        macroname = 'GenSMELLIE_run'+str(runNumber)+'subrun'+str(subRunNumber)+'.mac'
                        f = open(macroname,'w')
                        f.write('#Automatically generated macro to simulate SMELLIE run'+str(runNumber)+'subrun'+str(subRunNumber)+'\n')
                        f.write('/rat/physics_list/OmitMuonicProcesses true \n')
                        f.write('/rat/physics_list/OmitHadronicProcesses true \n')
                        f.write('/rat/db/set DAQ_RUN_LEVEL trigger_mask 32768 \n')
                        f.write('/rat/db/set DAQ_RUN_LEVEL trigger_enable 35967 \n')
                        f.write('/rat/db/set MC run '+str(runNumber)+'\n')
                        f.write('/rat/db/set MC subrun '+str(subRunNumber)+'\n')
                        f.write('/rat/db/set ELLIE intensity '+str(Nphotons)+'\n')
                        f.write('/rat/db/set ELLIE fibre_id "'+str(infoForSubRun['fibre'])+'"\n')
                        #Need to fix up laser name
                        f.write('/rat/db/set ELLIE wavelength_dist "SMELLIE'+str(infoForSubRun['laserWL'])+'"\n')
                        f.write('/rat/db/set ELLIE time_dist "SMELLIE'+str(infoForSubRun['laserWL'])+'"\n')
                        f.write('/rat/db/set ELLIE pulse_mode "poisson"\n')
                        f.write('/run/initialize\n')
                        f.write('# BEGIN EVENT LOOP\n')
                        f.write('/rat/proc frontend\n')
                        f.write('/rat/proc trigger\n')
                        f.write('/rat/proc eventbuilder\n')
                        f.write('/rat/proc calibratePMT\n')
                        f.write('/rat/proc outroot\n')
                        f.write('/rat/procset file "SMELLIE_'+str(infoForSubRun['fibre'])+'_'+str(infoForSubRun['laser'])+'.root"\n')
                        f.write('/rat/proc/if trigTypeSelector\n')
                        f.write('/rat/procset trigType "EXTASY"\n')
                        f.write('    /rat/proc socdata\n')
                        f.write('/rat/proc/endif\n')
                        f.write('/rat/proc outsoc\n')
                        f.write('/rat/procset file "SMELLIE_'+str(infoForSubRun['fibre'])+'_'+str(infoForSubRun['laser'])+'.soc.root"\n')
                        f.write('# END EVENTLOOP\n')
                        f.write('# Choose the LED generator\n')
                        f.write('/generator/add ellie\n')
                        f.write('/generator/rate/set '+str(runDescriptionInfo['trigger_frequency'])+'\n')
                        f.write('# simulate some events\n')
                        f.write('/rat/run/start '+str(runDescriptionInfo['triggers_per_loop'])+'\n')
                        f.write('exit\n')
                        f.close()
                    except:
                        print "SubRun number does not go this high " + str(subRunNumber) + "\t"
                        exists = 0
                        max_subrun = subRunNumber -1

print "DONE "+str(max_subrun)+" scripts generated for run "+ str(runNumber)+"\n"
