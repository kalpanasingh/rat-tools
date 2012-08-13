ZDAB to RAT ROOT Converter
==========================
Utilities for converting SNO/SNO+ ZDAB files or blobs into RAT ROOT objects.

Building
========
To build everything (except examples), run `make`. You can also choose to build a subset:

* `make zdab2root`: zdab2root tool and dependencies libzfile and libzconvert
* `make libzconvert`: libzconvert only
* `make libzfile`: libzfile only
* `make libzdispatch`: libconthost and libzdispatch
* `make examples`: everything, plus example code

Be sure to add `lib` to your `$LD_LIBRARY_PATH`, and also `contrib/disp/lib` if using libconthost. `env.sh` sets these for you. 

CLI Tools
=========
zdab2root
---------
CLI tool to convert ZDAB files (SNO or SNO+) to RAT ROOT files.

Usage:

    $ ./zdab2root SNO_00012345_000.zdab

By default, this will write to `SNO_00012345_000.root`. Override that by providing an output filename as a second argument.

libratzdab
==========
A C++ library for converting ZDAB blobs to RAT DS ROOT objects. `libratzdab` is a compilation of three libraries: `libzfile`, `libzconvert`, and `libzdispatch`. All of libratzdab lives in namespace `ratzdab`.

libzfile: ZDAB File I/O
-----------------------
`zdab_file.hpp` provides a class `file` to simplify reading ZDAB files.

It is constructed with a filename, and provides one method -- `next()`. This returns the next record in the file as a ROOT `TObject*`.

If an unknown record type is encountered, a `unknown_record_error` will be thrown.

If there is a problem reading the ZDAB file, `file` throws a `zdab_file_read_error`.

libzdispatch: ZDAB Dispatcher I/O
---------------------------------
`zdab_dispatch.hpp` provides a class `dispatch` to provide access to a dispatcher stream.

It is constructed with a hostname and, optionally, a subscription string describing which types of records should be received. The default subscription is `"w RAWDATA w RECHDR"`. As in `file`, the `next()` method returns the next record in the stream as a ROOT `TObject*`.

`dispatch::next` takes an optional boolean argument, `block`. If `block` is true (the default), `next` will wait until data is received until returning. If false, it will return immediately, `NULL` if no data is available.

If an unknown record type is encountered, a `unknown_record_error` will be thrown. If a record is encountered that is larger than the maximum allowed buffer size, an `insufficient_buffer_error` is thrown.

If there is a problem connecting, `dispatch` throws a `dispatcher_connection_error`.

libzconvert: ZDAB-ROOT Conversions
----------------------------------
`zdab_convert.hpp` provides the following conversion functions:

    RAT::DS::Root* unpack::event(PmtEventRecord* pev)
    RAT::DS::Run* unpack::rhdr(RunRecord* rhdr);
    RAT::DS::TRIGInfo* unpack::trig(TriggerInfo* trig);
    RAT::DS::EPEDInfo* unpack::eped(EpedRecord* eped);
    RAT::DS::ManipStat* unpack::cast(ManipStatus* cast);
    RAT::DS::AVStat* unpack::caac(AVStatus* caac);

The TRIG, EPED, CAST, and CAAC converters are not yet implemented.

Examples
--------
Example programs using libratzdab are provided in `examples`. See `examples/README.md` for details.

