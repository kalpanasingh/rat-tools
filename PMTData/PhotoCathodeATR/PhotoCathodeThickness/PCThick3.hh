////////////////////////////////////////////////////////
/// Optics0 RAT attempt
///
/// 05/08/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef PCThick3_hh
#define PCThick3_hh

#include <LinearInterpContainer.hh>
#include <math.h>

double
GetThickness3(
	      double z ) // In mm relative to PMT equator
{
  const double dynodeTop = -5.9;//-29.4;
  const double centreThickness = 27.99; //in nm
  const double topRq = ( 74.4 - dynodeTop ) * ( 74.4 - dynodeTop );
  double zDiff = z - dynodeTop;

  double rSq = 0.0;
  if( z > (96.6 - 50.9) ) // Z pos of sphere torroid change
    {
      double rhoSq = ( 125.3 * 125.3 - pow( z + 50.9, 2 ) );
      rSq = zDiff * zDiff + rhoSq;
    }
  else
    {
      double rho = 42.0 + sqrt( 59.2 * 59.2 - z * z );
      rSq = zDiff * zDiff + rho * rho;
    }
  double thick = centreThickness * topRq / rSq;


  return thick;
  /* OLD BELOW
  double zPos[] = { 75.00, 53.06, 5.00, 0.00, -25.00 };
  double thick[] = { 2.799e-05, 2.09499e-05, 1.77582e-05, 1.78969e-05, 1.91204e-05 };

  PHIL::LinearInterpContainer posVThick;
  posVThick.Add( zPos, thick, 5 );
  posVThick.Sort();

  return posVThick.InterpolateY( z ) * 1e6; // In nm not mm
  */
}

#endif
