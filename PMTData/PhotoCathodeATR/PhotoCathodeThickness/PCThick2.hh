////////////////////////////////////////////////////////
/// Optics 6b SNOMAN Thickness
///
/// 05/08/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef PCThick2_hh
#define PCThick2_hh

#include <math.h>

double
GetThickness2(
	      double z ) // In mm relative to PMT equator
{
  const double nominalThickness = 27.99; // in nm
  //const double thickFrac = 0.725;
  const double apmt_i = 71.4; //74.4 -3.0

  double zPrime2 = ( apmt_i - z ) / 10.0; 
  zPrime2 = zPrime2 * zPrime2;

  double thick = nominalThickness * ( ( 1.0 - 0.63 ) * exp( -0.1734 * zPrime2 ) + 0.63 ); //-0.1734

  return thick;
}

#endif
