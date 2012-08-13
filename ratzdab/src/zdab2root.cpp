/*********************************************************
 * ZDAB to RAT ROOT converter
 *
 * Converts SNO/SNO+ ZDAB files to full-DS RAT ROOT files,
 * including CAEN data if present. Currently SNOMAN MC,
 * fits, NCD data, and other SNO-specific things are
 * excluded.
 *
 * A. Mastbaum <mastbaum@hep.upenn.edu>, 8/2012
 *
 *********************************************************/
#include <TFile.h>
#include <TTree.h>

#include <RAT/DB.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>

#include <zdab_file.hpp>

int main(int argc, char* argv[]) {
    if (argc < 2 or argc > 3) {
        printf("Usage: %s input.zdab [output.root]\n", argv[0]);
        printf("If output filename is not specified, the input filename with a ROOT extension is used.\n");
        return 1;
    }
    // set up zdab input
    const char* infile = argv[1];
    ratzdab::file zdab(infile);

    // set up root output
    std::string outfile_name;
    if (argc > 2) {
        outfile_name = argv[2];
    }
    else {
        outfile_name = argv[1];
        outfile_name.erase(outfile_name.end()-5, outfile_name.end());
        outfile_name += ".root";
    }
    printf("Writing to %s\n", outfile_name.c_str());
    TFile outfile(outfile_name.c_str(), "recreate");
    outfile.cd();

    RAT::DS::Root* ds = new RAT::DS::Root();
    TTree* tree = new TTree("T", "RAT Tree");
    tree->Branch("ds", ds->ClassName(), &ds, 32000, 99);
    tree->SetAutoFlush(10);
    tree->SetAutoSave(10000);

    RAT::DS::Run* run = new RAT::DS::Run();
    TTree* runtree = new TTree("runT", "RAT Run Tree");
    runtree->Branch("run", run->ClassName(), &run, 32000, 99);

    // containers for data that spans multiple events
    RAT::DS::TRIGInfo* current_trig = NULL;
    RAT::DS::EPEDInfo* current_eped = NULL;

    unsigned record_count = 0;
    unsigned event_count = 0;
    bool run_active = false;
    bool run_level_data_set = false;

    while(true) {
        try {
            TObject* r = zdab.next();

            if (!r) {
                break;
            }

            // handle record types
            if (r->IsA() == RAT::DS::Run::Class()) {
                *run = *((RAT::DS::Run*) r);
                run_active = true;
                std::cout << "RHDR: Run " << run->GetRunID() << std::endl;
            }
            else if (r->IsA() == RAT::DS::Root::Class()) {
                *ds = *((RAT::DS::Root*) r);

                // some run-level data has to come from an event
                if (run_active && !run_level_data_set) {
                    run->SetSubRunID(ds->GetSubRunID());
                    run->SetMCFlag(0); // no mc zdabs
                    run->SetPackVer(0); // not in event, maybe MAST?
                    run->SetDataType(0); // ???
                }

                // set event headers if available
                RAT::DS::HeaderInfo* header = ds->GetHeaderInfo();

                if (current_trig) {
                    RAT::DS::TRIGInfo* triginfo = header->GetTRIGInfo();
                    *triginfo = *current_trig;
                }

                if (current_eped) {
                    RAT::DS::EPEDInfo* epedinfo = header->GetEPEDInfo();
                    *epedinfo = *current_eped;
                }

                tree->Fill();

                event_count++;
            }
            else {
                std::cerr << "Unhandled ROOT object of type " << r->ClassName() << std::endl;
            }

            if (record_count % 1000 == 0) {
                printf("Processed record %u (%u events)\n", record_count, event_count);
            }

        }
        catch(ratzdab::unknown_record_error& e) {
            if (VERBOSE) {
                std::cerr << e.what() << std::endl;
            }
        }

        record_count++;
    }

    outfile.cd();
    runtree->Fill();
    runtree->Write();
    tree->Write();
    outfile.Close();

    return 0;
}

