////////////////////////////////////////////////////////
/// Vanilla SNOMAN Thickness 
///
/// 05/08/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef PCThick1_hh
#define PCThick1_hh

double
GetThickness1(
	      double z ) // In mm relative to PMT equator
{
  const double nominalThickness = 27.99; // in nm
  double thick = nominalThickness;
  if( z < 45.0 )
    thick = nominalThickness * ( z + 95.0 ) / 140.0;
  return thick;
}

#endif
