////////////////////////////////////////////////////////
/// Seperate the ATR functions from the drawing functions
///
/// 27/02/11 - New file
////////////////////////////////////////////////////////

#include "ATRFunctions.hh"
#include <PHILCalcFunctions.hh>

void
CalculateTRThinFilm(
                    const double theta,
                    const double n1,
                    const complex<double> lN2,
                    const double n3,
                    const double energy,
                    const double pcThickness,
                    double& Ts,
                    double& Tp,
                    double& Rs,
                    double& Rp )
{
  const double wavelength = 299792458 * 4.13566733e-15 * 1e9 / energy;

  const complex<double> lN1( n1, 0.0 );
  const complex<double> lN3( n3, 0.0 );

  complex<double> cos1 = cos( theta );
  complex<double> sin1 = sin( theta );

  double eta = 2.0 * PHIL::kPI * pcThickness / wavelength;
  complex<double> ratio13sin = (lN1/lN3) * (lN1/lN3) * sin1 * sin1;
  complex<double> cos3 = sqrt( complex<double>( 1.0, 0.0 ) - ratio13sin );
  complex<double> ratio12sin = (lN1/lN2) * (lN1/lN2) * sin1 * sin1;
  complex<double> cos2 = sqrt( complex<double>( 1.0, 0.0 ) - ratio12sin );
  double u = real( lN2 * cos2 );
  double v = imag( lN2 * cos2 );

  complex<double> r12;
  complex<double> r23;
  complex<double> t12;
  complex<double> t23;
  complex<double> g;

  {
    // s Polarisation
    complex<double> n1c1 = lN1 * cos1;
    complex<double> n2c2 = lN2 * cos2;
    complex<double> n3c3 = lN3 * cos3;
    r12 = ( n1c1 - n2c2 ) / ( n1c1 + n2c2 );
    r23 = ( n2c2 - n3c3 ) / ( n3c3 + n2c2 );
    t12 = complex<double>( 2.0, 0.0 ) * n1c1 / ( n1c1 + n2c2 );
    t23 = complex<double>( 2.0, 0.0 ) * n2c2 / ( n2c2 + n3c3 );
    g = n3c3 / n1c1;

    double abs_r12 = abs( r12 );
    double abs_r23 = abs( r23 );
    double abs_t12 = abs( t12 );
    double abs_t23 = abs( t23 );
    double arg_r12 = arg( r12 );
    double arg_r23 = arg( r23 );
    double exp1 = exp( 2.0 * v * eta);

    ToTR( u, eta, g, abs_r12, abs_r23, abs_t12, abs_t23, arg_r12, arg_r23, exp1, Ts, Rs );
  }
  {
    // p Polarisation
    complex<double> n2c1 = lN2 * cos1;
    complex<double> n3c2 = lN3 * cos2;
    complex<double> n2c3 = lN2 * cos3;
    complex<double> n1c2 = lN1 * cos2;
    r12 = ( n2c1 - n1c2 ) / ( n2c1 + n1c2 );
    r23 = ( n3c2 - n2c3 ) / ( n3c2 + n2c3 );
    t12 = complex<double>( 2.0, 0.0 ) * lN1 * cos1 / ( n2c1 + n1c2 );
    t23 = complex<double>( 2.0, 0.0 ) * lN2 * cos2 / ( n3c2 + n2c3 );
    g = lN3 * cos3 / ( lN1 * cos1 );

    double abs_r12 = abs( r12 );
    double abs_r23 = abs( r23 );
    double abs_t12 = abs( t12 );
    double abs_t23 = abs( t23 );
    double arg_r12 = arg( r12 );
    double arg_r23 = arg( r23 );
    double exp1 = exp( 2.0 * v * eta);

    ToTR( u, eta, g, abs_r12, abs_r23, abs_t12, abs_t23, arg_r12, arg_r23, exp1, Tp, Rp );
  }
}

void
ToTR(
     const double u,
     const double eta,
     const complex<double> g,
     const double abs_r12,
     const double abs_r23,
     const double abs_t12,
     const double abs_t23,
     const double arg_r12,
     const double arg_r23,
     const double exp1,
     double& T,
     double& R )
{
  const double exp2 = 1/exp1;
  const double denom = exp1 + abs_r12 * abs_r12 * abs_r23 * abs_r23 * exp2 + 2.0f * abs_r12 * abs_r23 * cos( arg_r23 + arg_r12 + 2.0 * u * eta );
  R = abs_r12 * abs_r12 * exp1 + abs_r23 * abs_r23 *exp2 + 2.0 * abs_r12 * abs_r23 * cos( arg_r23 - arg_r12 + 2.0 * u * eta );
  R = R / denom;
  T = real( g ) * abs_t12 * abs_t12 * abs_t23 * abs_t23;
  T = T / denom;
}
