////////////////////////////////////////////////////////
/// Theorectical SNOMAN NK
///
/// 09/08/10 - Copied data, made new file
///////////////////////////////////////////////////////
#ifndef AluNK2_hh
#define AluNK2_hh

double
GetAluN2(
	 double energy ) // In eV
{
  //param_n1=18.020,param_n2=-22.208,param_n3=12.007,param_n4=-3.5144,param_n5=0.57948,param_n6=-0.050740,param_n7=0.0018383
  return 18.020 + energy * ( -22.208 + energy * ( 12.007 + energy * ( -3.5144 + energy * ( 0.57948 + energy * ( -0.050740 + energy * 0.0018383 ) ) ) ) );
}

double
GetAluK2(
	 double energy ) // In eV
{
  //param_k1=21.06,param_k2=-10.609,param_k3=1.8587,param_k4=0.24339,param_k5=-0.14669,param_k6=0.021117,param_k7=-0.0010415
  return 21.06 + energy * ( -10.609 + energy * ( 1.8587 + energy * ( 0.24339 + energy * ( -0.14669 + energy * ( 0.021117 + energy * -0.0010415 ) ) ) ) );
}

#endif
