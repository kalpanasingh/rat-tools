///////////////////////////////////////////////////////////////////////
//
// Using ntuple output files from special RAT simulation runs, generate tables
// of the probability of generating a PE in a PMT given a photon of a given
// wavelength and polarization incident on the PMT face at a given incidence
// angle.
//
// Author: W. Heintzelman <billh@hep.upenn.edu>
//
// REVISION HISTORY:
//     10/07/2016 : W. Heintzelman - New file
//
// DETAILS:
//    If, starting at the midpoint of the angular distribution for a given
//    wavelength/polarization, a non-zero value is found after a number of
//    zeroes, the non-zero value is distributed back equally over the preceding
//    angle bins that contained zeroes.
//
//    The program takes three command-line arguments.  The first is the number
//    of PMTs on-line in the RAT simulation runs.  The second is the directory
//    in which the RAT simulation output files are located The third is a
//    string that specifies what kind of output is desired.  Any combination of
//    the following three options is allowed:
//       c -- write outputs in form for copying into the RAT PEnergy.cc file
//       r -- write outputs at each wavelength/polarization as a function of
//            incidence angle, with the values normalized to one at
//            perpendicular incidence
//       p -- write results for use as input to a plotting routine.
//            Either for a given polarization and wavelength, pairs of
//            incidence angle and probability values; or for a given
//            polarization and incidence angle, pairs of wavelength and
//            probability values.
//
//     A typical command line to invoke the program might be
//        ./makePMTEffTable.exe   8927   ./output    c
////////////////////////////////////////////////////////////////////////

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <sstream>

#include <TFile.h>
#include <TROOT.h>
#include <TSystem.h>
#include <TTree.h>

// Convert an integer to a string
std::string IntToStr(int n) {
    std::stringstream ss;     //create a stringstream
    ss << n;             //add number to the stream
    return ss.str();     //return a string with the contents of the stream
}

using std::cout;
using std::string;
using std::endl;
using namespace ROOT;

// ----------------------------------------------

int main(int argc, char* argv[]) {
if(argc<2) {
    cout << "Input of number of on-line PMTs is required." << endl;
    exit(0);
}
double nOnLine = atof(argv[1]);
cout << "Number of on-line PMTs = " << nOnLine << endl;

if(argc<3) {
    cout<<"Input of directory containing RAT ntuple files is required." <<endl;
    exit(0);
}
string directory = argv[2];

bool printRel = false;
bool printCodeInput = false;
bool printPlotInput = false;
if(argc<4) {
    cout<<"Input of at least one output-type specification is expected." <<endl;
    exit(0);
}
string instring = argv[3];
printRel = (instring.find("r")!=string::npos);
printCodeInput = (instring.find("c")!=string::npos);
printPlotInput = (instring.find("p")!=string::npos);

gSystem->Load("libTree");       // necessary to avoid run-time error

const int nPol = 2;     // number of polarizations

// wavelengths -- first, last, and delta
const int firstL = 200;
const int lastL  = 800;
const int delL = 10;
const int nLambda= 1 + (lastL-firstL)/delL;

// incidence angles -- number and delta, in degrees beginning at zero
const int nAng = 46;
const int delA = 2;

double hitct[nPol][nLambda][nAng];
int nEvts[nPol][nLambda][nAng];

for (int i= 0; i<nPol; i++) {
    for (int j= 0; j<nLambda; j++) {
        for (int k= 0; k<nAng; k++) {
            hitct[i][j][k] = 0.;
            nEvts[i][j][k] = 0;
        }
    }
}

string polarization[2] = {"p","s"};
for (int ipol = 0; ipol<=1; ipol++)  {   // loop over polarizations
    string spol = polarization[ipol];
    int ilct=-1;
    // loop over wavelengths:
    for (int ilambda = firstL; ilambda<=lastL; ilambda+=delL)  {
        ilct++;             // wavelength counter
        string slambda = IntToStr(ilambda);
        int iact=-1;
        for (int iang = 0; iang<= 90; iang+=delA) {     // loop over angles
            iact++;         // angle counter
            string sang = IntToStr(iang);
            string filename =  directory + "/pmtEff" + slambda 
                                    + "_" + sang + "_" + spol + "-ntuple.root";
            // cout << "Reading file " << filename << endl;
            const char* fname = filename.c_str() ;
            Long_t *id, *size, *flags, *modtime;
            id = size = flags = modtime = NULL;
            // check if file exists:
            if(gSystem->GetPathInfo (fname, id, size, flags, modtime)==0) {
                TFile infile( fname );
                if (!infile.IsZombie()) {    // check if file is good

                    float mc_id, mc_pehitct, mc_pect, mc_dirpehitct ;
                    TTree* hitNtple = NULL; 
                    hitNtple = (TTree*)infile.Get("hitcount");
                    hitNtple->SetBranchAddress("mc_id", &mc_id);
                    hitNtple->SetBranchAddress("mc_pehitct", &mc_pehitct);
                    hitNtple->SetBranchAddress("mc_pect", &mc_pect);
                    hitNtple->SetBranchAddress("mc_dirpehitct", &mc_dirpehitct);

                    float oldId = -1.;
                    Int_t nentries = (Int_t)hitNtple->GetEntries();

                    for (Int_t i=0; i<nentries; i++) {
                        hitNtple->GetEntry(i);
                        if (mc_id != oldId) {       // avoid retriggers?
                            hitct[ipol][ilct][iact] += mc_dirpehitct;
                            nEvts[ipol][ilct][iact]++;
                        }
                        oldId = mc_id;
                    }

//                     cout<<"File "<<filename<<"    Events, total hit count = "
//                         << nEvts[ipol][ilct][iact] <<" "
//                         << hitct[ipol][ilct][iact] << endl;
                }else{
                    cout<<"File " << filename << " bad."<< endl;
                    hitct[ipol][ilct][iact] = 0;
                    nEvts[ipol][ilct][iact] = 1;
                }       // if (!infile.IsZombie()) 

            }else{
                cout<<"File " << filename << " not found."<< endl;
                hitct[ipol][ilct][iact] = 0;
                nEvts[ipol][ilct][iact] = 1;
            }       // if file exists
        }           // for (int iang = 0; iang<= 90-delA; iang+=delA)
    }               // for (int ilambda = firstL; ilambda<=lastL; ilambda+=delL)
}               // for (int ipol = 0; ipol<=1; pol++)

cout << endl << endl;


for (int ipol = 0; ipol<=1; ipol++)  {   // loop over polarizations
    // Starting at midpoint of angular distribution, if a non-zero value is
    // found after a number of zeroes, spread the distribution back over the
    // preceding zeroes.
    for (int ilct = 0; ilct<nLambda; ilct++) {

        int lastzeroseq = -1;  // index of beginning of last sequence of zeroes
        for (int iact = 0; iact<nAng; iact++) {
            if(hitct[ipol][ilct][iact]==0.) {
                if(lastzeroseq==-1) lastzeroseq = iact;
            }else{                  //  if(hitct[ipol][ilct][iact]!=0.) 
                if(iact<nAng/2) {
                    lastzeroseq = -1;
                }else{
                    if(lastzeroseq>=0 ) {
                        double avg = hitct[ipol][ilct][iact]/
                                                (double)(iact-lastzeroseq+1);
                        for (int k = lastzeroseq; k<=iact; k++) {
                            hitct[ipol][ilct][k] = avg;
                        }
                        lastzeroseq = -1;
                    }
                }
            }
        }
    }
}

if( printRel ) {
    // Print table of response relative to perpendicular incidence --
    cout << endl;
    cout << "Tables of response normalized to 1 at perpendicular incidence --" 
                                                                    << endl;
    for (int ipol = 0; ipol<=1; ipol++)  {   // loop over polarizations
        cout << endl;
        cout << "{" << endl;
        for (int ilct = 0; ilct<nLambda; ilct++) {
            cout << "{" ;
            for (int iact = 0; iact<nAng; iact++) {
                double denom = hitct[ipol][ilct][0];
                if(denom == 0.) denom = 1.e-7;
                double val = hitct[ipol][ilct][iact]/denom;
                if(val<1.e-7) val = 1.e-7;
                if(val<1.e-5) {
                    printf("%9.2e", val);
                }else{
                    printf("%9.7f", val);
                }
                if(iact!=nAng-1) cout << "," ;
            }
            if(ilct!=nLambda-1) {
                cout << "},\n" ;
            }else{
                cout << "}};\n" ;
            }
        }
        cout << endl;
    }
}

if( printCodeInput ) {
    cout << endl;
    cout << "// For copying into PEnergy.cc, absolute response --" << endl;
    cout << "{" << endl;
    for (int ipol = 0; ipol<=1; ipol++)  {   // loop over polarizations
        // For copying into PEnergy.cc, absolute response --
        cout << "{" << endl;
        for (int ilct = 0; ilct<nLambda; ilct++) {
            cout << "{" ;
            for (int iact = 0; iact<nAng; iact++) {
                double f = 0.;
                if( nEvts[ipol][ilct][iact] > 0 ) {
                    f = 1./((double)nEvts[ipol][ilct][iact]*nOnLine);
                }
                double val = f*hitct[ipol][ilct][iact];
                if( val<1.e-7 ) val = 1.e-7;
                if( val<1.e-5 ) {
                    printf("%9.2e", val);
                }else{
                    printf("%9.7f", val);
                }
                if(iact!=nAng-1) cout << "," ;
            }
            if(ilct!=nLambda-1) {
                cout << "},\n" ;
            }else{
                cout << "}\n" ;
            }
        }
        if(ipol!=1) {
            cout << "},\n\n" ;
        }else{
            cout << "}\n" ;
        }
    }
    cout << "};\n" ;
    cout << endl;
}

if( printPlotInput ) {
    for (int ipol = 0; ipol<=1; ipol++)  {   // loop over polarizations
        // For making plots  of response vs. angle--
        cout << endl;
        cout << " For making plots  of response vs. angle--" << endl;
        string spol = polarization[ipol];
        // for (int ilct = 0; ilct<nLambda; ilct++) {
        for (int ilct = 5; ilct<=50; ilct+=5) {
            cout << "# Polarization = "<< spol << 
                    "       Lambda = "<< firstL+ilct*delL << endl ;
            for (int iact = 0; iact<nAng; iact++) {
                cout <<  iact*delA <<" ";
            }
            cout << "EndX" << endl;
            for (int iact = 0; iact<nAng; iact++) {
                double f = 0.;
                if( nEvts[ipol][ilct][iact] > 0 ) {
                    f = 1./((double)nEvts[ipol][ilct][iact]*nOnLine);
                }
                double val = f*hitct[ipol][ilct][iact];
                if( val<1.e-7 ) val = 1.e-7;
                if( val<1.e-5 ) {
                    printf("%9.2e ", val);
                }else{
                    printf("%9.7f ", val);
                }
            }
            cout << "EndY" << endl << endl;
        }
        cout << endl;
    }

    for (int ipol = 0; ipol<=1; ipol++)  {   // loop over polarizations
        // For making plots  of response vs. wavelength --
        cout << endl;
        cout << " For making plots  of response vs. wavelength --" << endl;
        string spol = polarization[ipol];
        for (int iact = 0; iact<nAng; iact+=5) {
            cout << "# Polarization = "<< spol << 
                    "       Angle = "<< iact*delA << endl;
            for (int ilct = 0; ilct<nLambda; ilct++) {
                cout <<  firstL+ilct*delL <<" ";
            }
            cout << "EndX" << endl;
            for (int ilct = 0; ilct<nLambda; ilct++) {
                double f = 0.;
                if( nEvts[ipol][ilct][iact] > 0 ) {
                    f = 1./((double)nEvts[ipol][ilct][iact]*nOnLine);
                }
                double val = f*hitct[ipol][ilct][iact];
                if( val<1.e-7 ) val = 1.e-7;
                if( val<1.e-5 ) {
                    printf("%9.2e ", val);
                }else{
                    printf("%9.7f ", val);
                }
            }
            cout << "EndY" << endl << endl;
        }
        cout << endl;
    }
}

return 0;
}

