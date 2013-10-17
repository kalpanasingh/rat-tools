/*********************************************************
 * ZDAB to RAT ROOT converter
 *
 * Converts SNO/SNO+ ZDAB files to full-DS RAT ROOT files
 *
 * A. Mastbaum <mastbaum@hep.upenn.edu>, 8/2012
 *********************************************************/
#include <zdab_file.hpp>
#include <iostream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include <RAT/DB.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DS/TRIGInfo.hh>
#include <RAT/DS/EPEDInfo.hh>
#include <RAT/DS/AVStat.hh>
#include <RAT/DS/ManipStat.hh>

int main(int argc, char* argv[]) {
    if (argc < 2 || argc > 3) {
        std::cout << "Usage: " << argv[0] << " input.zdab [output.root]"
                  << std::endl
                  << "If output filename is not specified, the input filename "
                  << "with a ROOT extension is used."
                  << std::endl;
        return 1;
    }

    // set up zdab input
    const char* infile = argv[1];
    ratzdab::zdabfile zdab(infile);

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
    std::cout << "Writing to " << outfile_name << std::endl;
    TFile outfile(outfile_name.c_str(), "recreate");
    outfile.cd();

    RAT::DS::Root* ds = new RAT::DS::Root();
    TTree* tree = new TTree("T", "RAT Tree");
    tree->Branch("ds", ds->ClassName(), &ds, 32000, 99);

    RAT::DS::Run* run = new RAT::DS::Run();
    TTree* runtree = new TTree("runT", "RAT Run Tree");
    runtree->Branch("run", run->ClassName(), &run, 32000, 99);

    // containers for data that spans multiple events
    RAT::DS::TRIGInfo* current_trig = static_cast<RAT::DS::TRIGInfo*>(NULL);
    RAT::DS::EPEDInfo* current_eped = static_cast<RAT::DS::EPEDInfo*>(NULL);

    unsigned record_count = 0;
    unsigned event_count = 0;
    bool run_active = false;
    bool run_level_data_set = false;

    while (true) {
        try {
            TObject* r = zdab.next();

            if (!r) {
                break;
            }

            // handle record types
            if (r->IsA() == RAT::DS::Run::Class()) {
                *run = *(dynamic_cast<RAT::DS::Run*>(r));
                run_active = true;
                std::cout << "RHDR: Run " << run->GetRunID() << std::endl;
            }
            else if (r->IsA() == RAT::DS::AVStat::Class()) {
                if (run_active) {
                    RAT::DS::AVStat* avstat = run->GetAVStat();
                    *avstat = *(dynamic_cast<RAT::DS::AVStat*>(r));
                    std::cout << "AVStat: Run updated" << std::endl;
                }
                else {
                    std::cerr << "Warning: Ignoring AVStat since there is no run active" << std::endl;
                }
            }
            else if (r->IsA() == RAT::DS::ManipStat::Class()) {
                if (run_active) {
                    RAT::DS::ManipStat* mstat = run->GetManipStat();
                    *mstat = *(dynamic_cast<RAT::DS::ManipStat*>(r));
                    std::cout << "ManipStat: Run updated" << std::endl;
                }
                else {
                    std::cerr << "Warning: Ignoring ManipStat since there is no run active" << std::endl;
                }
            }
            else if (r->IsA() == RAT::DS::TRIGInfo::Class()) {
                delete current_trig;
                current_trig = dynamic_cast<RAT::DS::TRIGInfo*>(r);

                if (run_active) {
                    current_trig->SetRunID(run->GetRunID());
                }

                std::cout << "TRIG: GTID " << current_trig->GetEventID() << std::endl;
            }
            else if (r->IsA() == RAT::DS::EPEDInfo::Class()) {
                delete current_eped;
                current_eped = dynamic_cast<RAT::DS::EPEDInfo*>(r);

                if (run_active) {
                    current_eped->SetRunID(run->GetRunID());
                }

                std::cout << "EPED: GTID " << current_eped->GetEventID() << std::endl;
            }
            else if (r->IsA() == RAT::DS::Root::Class()) {
                *ds = *(dynamic_cast<RAT::DS::Root*>(r));

                // some run-level data has to come from an event
                if (run_active && !run_level_data_set) {
                    run->SetMCFlag(0);  // no mc zdabs
                    run->SetPackVer(0);  // not in event, maybe MAST?
                    run->SetDataType(0);  // ???

                    run_level_data_set = true;
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
            else if (r->IsA() == TObject::Class()) {
                //a record has been swallowed by converter on purpose
            }
            else {
                std::cerr << "Unhandled ROOT object of type " << r->ClassName() << std::endl;
            }

            if (record_count % 1000 == 0) {
                std::cout << "Processed record " << record_count
                          << " (" << event_count << " events)" << std::endl;
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

