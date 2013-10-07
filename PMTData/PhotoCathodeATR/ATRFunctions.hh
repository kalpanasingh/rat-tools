////////////////////////////////////////////////////////
/// Seperate the ATR functions from the drawing functions
///
/// 27/02/11 - New file
////////////////////////////////////////////////////////

#ifndef ATRFunctions_hh
#define ATRFunctions_hh

#include <complex>
using namespace std;

void
CalculateTRThinFilm(
                    const double theta,
                    const double lN1,
                    const complex<double> lN2,
                    const double lN3,
                    const double energy,
                    const double pcThickness,
                    double& Ts,
                    double& Tp,
                    double& Rs,
                    double& Rp );
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
     double& R );


#endif
