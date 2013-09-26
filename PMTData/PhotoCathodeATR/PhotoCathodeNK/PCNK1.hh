////////////////////////////////////////////////////////
/// SNOMAN NK
///
/// 10/08/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef PCNK1_hh
#define PCNK1_hh

double
GetPCN1(
	 double energy ) // In eV
{
  //param_pcath_n1=8.493,param_pcath_n2=-9.6372,param_pcath_n3=5.2069,param_pcath_n4=-0.8822
  if( energy > 3.2 )
    energy = 3.2;
  double n = 8.493 + energy * ( -9.6372 + energy * ( 5.2069 + energy * -0.8822 ) );
  if( energy > 3.0 && n < 0.5 )
    n = 0.5;
  else if( energy < 3.0 && n < 0.1 )
    n = 0.1;
  return n;
}

double
GetPCK1(
	 double energy ) // In eV
{
  //param_pcath_k1=5.6859,param_pcath_k2=-8.4885,param_pcath_k3=3.9397,param_pcath_k4=-0.5139
  if( energy > 3.2 )
    energy = 3.2;
  double k = 5.6859 + energy * ( -8.4885 + energy * ( 3.9397 + energy * -0.5139 ) );
  if( energy > 3.0 && k < 0.5 )
    k = 0.5;
  else if( energy < 3.0 && k < 0.1 )
    k = 0.1;
  return k;
}

#endif
