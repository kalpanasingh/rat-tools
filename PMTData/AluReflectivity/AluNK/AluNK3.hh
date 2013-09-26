////////////////////////////////////////////////////////
/// Optics0 RAT attempt, data from http://refractiveindex.info/?group=METALS&material=Aluminium
///
/// 09/08/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef AluNK3_hh
#define AluNK3_hh

#include <LinearInterpContainer2.hh>

double
GetAluN3(
	 double energy ) // In eV
{
  double wavelength[] = { 60.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0 };
  double n[] = { 0.70098, 0.11945, 0.26418, 0.48787, 0.81257, 1.26232, 1.92139, 2.76733 };

  const double conversionFactor = 299792458 * 4.13566733e-15 * 1e9; // E [eV]= conversionFactor / wavelength [nm]
  double energyA[8];
  for( int iLoop = 0; iLoop < 8; iLoop++ )
    {
      energyA[iLoop] = conversionFactor / wavelength[iLoop];
    }

  PHIL::LinearInterpContainer2 energyVN;
  energyVN.Add( energyA, n, 8 );
  energyVN.Sort();

  return energyVN.InterpolateY( energy );
}

double
GetAluK3(
	 double energy ) // In eV
{
  double wavelength[] = { 60.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0 };
  double k[] = { 0.021304, 2.26534, 3.57873, 4.83552, 6.04806, 7.18550, 8.14197, 8.35432 };

  const double conversionFactor = 299792458 * 4.13566733e-15 * 1e9; // E [eV]= conversionFactor / wavelength [nm]
  double energyA[8];
  for( int iLoop = 0; iLoop < 8; iLoop++ )
    {
      energyA[iLoop] = conversionFactor / wavelength[iLoop];
    }

  PHIL::LinearInterpContainer2 energyVK;
  energyVK.Add( energyA, k, 8 );
  energyVK.Sort();

  return energyVK.InterpolateY( energy );
}

#endif
