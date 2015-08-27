# Tools to create macros to simulate SMELLIE subruns

Since rat does not have sub-run level capability, the easiest way to simulate the 
separate subruns for a SMELLIE run (new subrun when intensity, wavelength or fibre 
changed in a SMELLIE scan) is to query the SMELLIE database directly and create a macro 
to simulate each subrun as a separate job.

The script CreateMacrosForSMELLIERun.py is well documented in the code but is not yet 
final as the intensity -> Nphotons mapping must be fixed (placeholder currently).

