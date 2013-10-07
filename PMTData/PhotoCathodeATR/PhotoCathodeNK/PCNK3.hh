////////////////////////////////////////////////////////
/// Optics0 RAT attempt, from arXiv:physics/0408075v1 17 Aug 2004
///
/// 10/08/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef PCNK3_hh
#define PCNK3_hh

#include <LinearInterpContainer2.hh>

double
GetPCN3(
	 double energy ) // In eV
{
  const int numVals = 22;
  double wavelength[] = { 60, 380, 395, 410, 425, 440, 455, 470, 485, 500, 515, 530, 545, 560, 575, 590, 605, 635, 650, 665, 680, 800 };
  double n[] = { 1.92, 2.18, 2.38, 2.61, 2.70, 2.87, 3.00, 3.00, 3.00, 3.09, 3.26, 3.20, 3.12, 3.06, 3.01, 2.98, 2.96, 2.95, 2.95, 2.95, 2.96, 2.96 };

  const double conversionFactor = 299792458 * 4.13566733e-15 * 1e9; // E [eV]= conversionFactor / wavelength [nm]
  double energyA[numVals];
  for( int iLoop = 0; iLoop < numVals; iLoop++ )
    {
      energyA[iLoop] = conversionFactor / wavelength[iLoop];
    }

  PHIL::LinearInterpContainer2 energyVN;
  energyVN.Add( energyA, n, numVals );
  energyVN.Sort();

  return energyVN.InterpolateY( energy );
}

double
GetPCK3(
	 double energy ) // In eV
{
  const int numVals = 22;
  double wavelength[] = { 60, 380, 395, 410, 425, 440, 455, 470, 485, 500, 515, 530, 545, 560, 575, 590, 605, 635, 650, 665, 680, 800 };
  double k[] = { 1.69, 1.69, 1.71, 1.53, 1.50, 1.44, 1.34, 1.11, 1.06, 1.05, 0.86, 0.63, 0.53, 0.46, 0.42, 0.38, 0.37, 0.35, 0.34, 0.34, 0.33, 0.33 };

  const double conversionFactor = 299792458 * 4.13566733e-15 * 1e9; // E [eV]= conversionFactor / wavelength [nm]
  double energyA[numVals];
  for( int iLoop = 0; iLoop < numVals; iLoop++ )
    {
      energyA[iLoop] = conversionFactor / wavelength[iLoop];
    }

  PHIL::LinearInterpContainer2 energyVK;
  energyVK.Add( energyA, k, numVals );
  energyVK.Sort();

  return energyVK.InterpolateY( energy );
}

#endif
