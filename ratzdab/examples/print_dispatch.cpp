#include <iostream>
#include <string>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <TObject.h>
#include <zdab_dispatch.hpp>

int main(int argc, char* argv[]) {
    std::string hostname;
    if (argc == 2) {
        hostname = std::string(argv[1]);
    }
    else {
        std::cerr << "Usage: " << argv[0] << " [hostname]" << std::endl;
        return 1;
    }

    // if connection fails, it will throw an exception
    std::cout << "Connecting to " << hostname << std::endl;
    ratzdab::dispatch client("snoplusbuilder1.snolab.ca");

    std::cout << "Listening..." << std::endl;
    TObject* o = NULL;

    // next() can throw an unknown record type exception, which should
    // really be handled.
    while (o = client.next()) {
        std::cout << "Received " << o->GetName() << ", ";

        // cast to the right root type and do something
        if (o->IsA() == RAT::DS::Run::Class()) {
            std::cout << "Run ID: " << ((RAT::DS::Run*)o)->GetRunID() << std::endl;
        }
        else if (o->IsA() == RAT::DS::Root::Class()) {
            std::cout << "NHIT: " << ((RAT::DS::Root*)o)->GetEV(0)->GetPMTUnCalCount();
        }

        std::cout << std::endl;

        // we own the TObject pointer
        delete o;
    }

    std::cout << "Stream terminated" << std::endl;

    return 0;
}

