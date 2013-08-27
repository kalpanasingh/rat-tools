////////////////////////////////////////////////////////
/// As Lay, but interpolated
///
/// 29/11/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef PCNK4_hh
#define PCNK4_hh

#include <LinearInterpContainer2.hh>

double
GetPCN4(
	 double energy ) // In eV
{
  const int numVals = 22;
  double wavelength[] = { 60.0, 375.0, 390.0, 405.0, 420.0, 435.0, 450.0, 465.0, 480.0, 495.0, 510.0, 525.0, 540.0, 555.0, 570.0, 585.0, 600.0, 615.0, 630.0, 645.0, 660.0, 675.0, 690.0, 705.0, 720.0, 735.0, 750.0, 765.0, 780.0, 795.0, 810.0, };
  double n[] = { 2.06469, 2.06469, 2.13336, 2.47674, 2.72348, 2.89703, 3.01518, 3.09152, 3.13645, 3.15799, 3.16228, 3.15407, 3.13704, 3.114, 3.08714, 3.05813, 3.02822, 2.99839, 2.96937, 2.94167, 2.91569, 2.8917, 2.86987, 2.85031, 2.83307, 2.81817, 2.8056, 2.79529, 2.7872, 2.78124, 2.77734 };

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
GetPCK4(
	 double energy ) // In eV
{
  const int numVals = 22;
  double wavelength[] = { 60.0, 375.0, 390.0, 405.0, 420.0, 435.0, 450.0, 465.0, 480.0, 495.0, 510.0, 525.0, 540.0, 555.0, 570.0, 585.0, 600.0, 615.0, 630.0, 645.0, 660.0, 675.0, 690.0, 705.0, 720.0, 735.0, 750.0, 765.0, 780.0, 795.0, 810.0 };
  double k[] = { 2.03024, 2.03024, 2.01387, 1.88742, 1.75012, 1.60874, 1.46795, 1.33095, 1.19985, 1.07599, 0.96015, 0.85272, 0.75382, 0.66337, 0.58113, 0.50681, 0.44005, 0.38044, 0.32757, 0.28102, 0.2404, 0.20529, 0.17531, 0.15009, 0.12929, 0.11258, 0.1, 0.1, 0.1, 0.1, 0.1 };

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
