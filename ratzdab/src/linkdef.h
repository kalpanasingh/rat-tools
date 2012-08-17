/** Generate CINT dictionary to wrap libratzdab for PyROOT */

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ nestedtypedefs;
#pragma link C++ nestedclasses;

// utility classes and exceptions
#pragma link C++ class ratzdab::dispatch!;
#pragma link C++ class ratzdab::zdabfile!;
#pragma link C++ class ratzdab::zdabfile::zdab_file_read_error!;
#pragma link C++ class ratzdab::dispatcher_connection_error!;
#pragma link C++ class ratzdab::insufficient_buffer_error!;
#pragma link C++ class ratzdab::unknown_record_error!;

// stl
#pragma link C++ class std::exception!;

// sno structs
#pragma link C++ struct PmtEventRecord!;
#pragma link C++ struct RunRecord!;
#pragma link C++ struct ManipStatus!;
#pragma link C++ struct ManipRopeStatus!;
#pragma link C++ struct AVStatus!;
#pragma link C++ struct TriggerInfo!;
#pragma link C++ struct EpedRecord!;

// unpacking functions
#pragma link C++ function ratzdab::unpack::event(PmtEventRecord*);
#pragma link C++ function ratzdab::unpack::rhdr(RunRecord*);
#pragma link C++ function ratzdab::unpack::cast(ManipStatus*);
#pragma link C++ function ratzdab::unpack::caac(AVStatus*);
#pragma link C++ function ratzdab::unpack::trig(TriggerInfo*);
#pragma link C++ function ratzdab::unpack::eped(EpedRecord*);
#pragma link C++ function ratzdab::unpack::caen(uint32_t*);
#pragma link C++ function ratzdab::unpack::pmt(uint32_t*);
#pragma link C++ class ratzdab::unpack;

// packing functions
#pragma link C++ function ratzdab::pack::event(RAT::DS::Root*, int);
#pragma link C++ function ratzdab::pack::rhdr(RAT::DS::Run*);
#pragma link C++ function ratzdab::pack::cast(RAT::DS::ManipStat*);
#pragma link C++ function ratzdab::pack::caac(RAT::DS::AVStat*);
#pragma link C++ function ratzdab::pack::trig(RAT::DS::TRIGInfo*);
#pragma link C++ function ratzdab::pack::eped(RAT::DS::EPEDInfo*);
#pragma link C++ class ratzdab::pack;

#endif

