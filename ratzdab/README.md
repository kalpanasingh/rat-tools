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

Testing
-------
Testing your installation is recommended:

    $ cd tests
    $ python -m unittest discover

Note: This requires that the `ratzdab` module be in your `PYTHONPATH`. Sourcing `env.sh` will do that for you.

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
`zdab_file.hpp` provides a class `zdabfile` to simplify reading ZDAB files.

It is constructed with a filename, and provides one method -- `next()`. This returns the next record in the file as a ROOT `TObject*`.

If an unknown record type is encountered, a `unknown_record_error` will be thrown.

If there is a problem reading the ZDAB file, `zdabfile` throws a `zdab_file_read_error`.

libzdispatch: ZDAB Dispatcher I/O
---------------------------------
`zdab_dispatch.hpp` provides a class `dispatch` to provide access to a dispatcher stream.

It is constructed with a hostname and, optionally, a subscription string describing which types of records should be received. The default subscription is `"w RAWDATA w RECHDR"`. As in `zdabfile`, the `next()` method returns the next record in the stream as a ROOT `TObject*`.

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

Python Interface
================
The `ratzdab` library can also be used from Python by importing `python/ratzdab.py`.

```python
>>> import ratzdab
RAT: Libraries loaded.
>>> f = ratzdab.zdabfile('SNO_0000020644_002.zdab')
>>>  o = f.next() # MAST record will fail
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
Exception: Unable to convert unknown record type. (C++ exception)
>>>> o = f.next()
>>> o
<ROOT.RAT::DS::Run object ("RAT::DS::Run") at 0x215acd0>
>>> o.runID
20644
```

This Python library is simply `libratzdab` wrapped by PyROOT, so the interface is identical. Specifically, `ratzdab` provides:

* `ratzdab.zdabfile(filename)`: A `ratzdab::zdabfile` ZDAB file interface object
* `ratzdab.dispatch(hostname, block=True)`: A `ratzdab::dispatch` ZDAB dispatcher interface object
* `ratzdab.pack`: Packing functions from `ratzdab::pack`
* `ratzdab.unpack`: Unpacking functions from `ratzdab::unpack`

SNO struct types are available in `ratzdab.ROOT` and RAT ROOT types are found in `ratzdab.ROOT.RAT`.

