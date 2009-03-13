/// SASQUATCH TOOL: Optics_SNOMAN_to_RAT
///
/// This file contains a series of methods to convert from SNOMAN optics format into 
/// RAT format. The input and output distributions are plotted and the text in RAT 
/// format is written to screen so that it can be cut-and-paste into the OPTICS.ratdb file
/// Note, for parameters where an _option is required, it should be set to "wavelength".
///
/// First version
/// auhor: Jeanne Wilson (Oxford)
/// date:  13/11/08
///

///-----------------------------------------------------------------------------------------///
/// Helper method to make plots look nice ;)
void SetUp(){
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(1);
	gStyle->SetTitleBorderSize(0);
}

///-----------------------------------------------------------------------------------------///
/// Typing Help tells you what methods are available and a brief summary of inputs and outputs
void Help(){
	cout << "SetUP() \n\t\t: set some style options for plots " << endl;
	cout << "RefIndex(double *RI) " 
	     << "\n\t\t: input array of 3 parameters for Refractive Index polynomial" 
		 << "\n\t\t-> array of 31 wavelengths and corresponding Refractive Index values " 
		 << endl;
	cout << "AbsScatNonScint(int ninp, double *wave, double *abscoeff, double RSfactor, double meanRI, double isocomp)"
		 << "\n\t\t: input number of points, arrays of wavelength and corresponding SNOMAN absorption coefficient, "
		 << "\n\t\t  SNOMAN Rayleigh scale factor, mean refractive index, and isothermal compressibility " 
		 << "\n\t\t-> array of 31 wavelengths and corresponding total extinction length in mm " 
		 << "\n\t\t  and corresponding arrays for fraction of extinction attributed to optical scattering " 
		 << endl;
	cout << "AbsScatRemScint(int nScintComp, double *relCont, double RSfactor, double meanRI, double isocomp, char *filenames[50], double *remprob)"
	     << "\n\t\t: input number of scintillator components, their relative contributions,"
		 << "\n\t\t: SNOMAN  Rayleigh scale factor, mean refractive index, and isothermal compressibility, " 
		 << "\n\t\t: array of filenames for the absorption properties of each scint component,"
		 << "\n\t\t: array of average reemision probability values for each scintillator component."
		 << "\n\t\t-> array of 41 wavelengths and corresponding total extinction length, optical scattering fraction "
		 << "\n\t\t   and reemission probability.	" 
		 << endl;
	cout << "ScintEmissionSpec(char filename[50]) "
		 << "\n\t\t: input the name of textfile containing the 200 values specifying spectrum" 
		 << "\n\t\t-> array of 41 wavelengths and corresponding primary emission intensities" << endl;
	cout << "ScintReemissionSpec(char filename[50]) "
	     << "\n\t\t: input the name of textfile containing the 401 values specifying reemission spectrum" 
		 << "\n\t\t-> array of 41 wavelengths and corresponding reemission intensities" 
		 << endl;
	cout << "FormatRatD(double val) "
		 << "\n\t\t: input a double value"
		 << "\n\t\t-> returns string in ratdb format" 
		 << endl; 
	cout << "Attenuation(double val) " 
		 << "\n\t\t: input a double value for SNOMAN absorption coeff in cm^-1"
		 << "\n\t\t-> double value for RAT absorption mean free path in mm."
		 << endl;
}

///-----------------------------------------------------------------------------------------///
/// Method to convert from the polynomial definition of refractive index in SNOMAN's 
/// media.dat file to a wavelength dependent array, RINDEX, in RAT format
void RefIndex(double *RI){
/// Arguments:
	/// RI 			= pointer to a double array of 3 values defining the refractive index
	/// 			polynomial, taken from media.dat
	
/// Output graphs:
	/// gRIsnoman	= graph of the input data refractive index vs wavelength
	/// gRIRAT		= graph of the output data refractive index vs wavelength (showing 
	///				any interpolation applied
	
/// Output text:
	///	RINDEX_value1	= array of wavelengths in nm
	/// RINDEX_value2	= corresponding array of RI values

/// Parameters:
	double lo_wave 			= 200;		// starting wavelength 
	double hi_wave 			= 800;		// last wavelength 
	const int nvals_output 	= 31;		// how many values do we want to output?
	bool verbose 			= false;	// output more info if true 

	// Set up the function
	TF1 *fRI = new TF1("fRI","[0]+[1]*exp([2]*1243.125/x)",200,800) ;
	fRI->SetParameters(RI[0], RI[1], RI[2]);
	TCanvas *CRI = new TCanvas("CRI");
	CRI->cd();
	fRI->SetLineWidth(2);
	fRI->SetLineColor(1);
	fRI->GetXaxis()->SetTitle("wavelength (nm)");
	fRI->GetYaxis()->SetTitle("refractive index");
	fRI->Draw();
	
	// Now extract the output parameters
	double wave[nvals_output];
	double RIout[nvals_output];
	double wave_step = (hi_wave-lo_wave)/(nvals_output-1);
	for(int i=0; i<nvals_output; ++i){
		wave[i] = lo_wave + i*wave_step;
		RIout[i] = fRI->Eval(wave[i]);
	}
	// Draw these points as a graph
	TGraph *gRI = new TGraph(nvals_output,wave,RIout);
	gRI->SetMarkerStyle(20);
	gRI->SetMarkerColor(2);
	gRI->SetLineColor(2);
	CRI->cd(2);
	gRI->Draw("PL");
	TLegend *legRI = new TLegend(0.6,0.7,0.89,0.89);
	legRI->SetBorderSize(0);
	legRI->SetFillColor(0);
	legRI->AddEntry(fRI,"input function","L");
	legRI->AddEntry(gRI,"output values", "PL");
	legRI->Draw();

	// Now to output the text in RAT format
	cout << "RINDEX_option: \"wavelength\"," << endl;
	cout << "RINDEX_value1: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(wave[i]) << ", ";	
	}
	cout << "], " << endl;
	cout << "RINDEX_value2: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(RIout[i]) << ", ";	
	}
	cout << "], " << endl;
}

///-----------------------------------------------------------------------------------------///
/// This method applies to non-scintillator materials where the absorption coefficients
/// are supplied as an array of up to 15 values in media.dat. This method combines
/// absorption with Rayleigh scattering (specified via a scale factor, a mean refractive
/// index and isothermal compressibility in media.dat) to obtain and overall extinction 
/// length, ABSLENGTH (mm). The fraction of this extinction that is due to scattering is 
/// output as the OPSCATFRAC array.
void AbsScatNonScint(int ninp, double *wave, double *abscoeff, double RSfactor, double meanRI, 
                     double isocomp){
/// Arguments:
	/// ninp		= number of input points
	/// wave 		= pointer to double array of up to 15 wavelengths
	/// abscoeff 	= pointer to double array of up to 15 corresponding absorption 
	///           	coefficients (in cm-1), taken from media.dat
	/// RSfactor 	= Rayleigh Scattering scale factor from media.dat
	/// meanRI 		= mean refractive index for this material, taken from media.dat
	/// isocomp 	= Isothermal Compressibility of the material, taken from media.dat
	
/// Output histograms and graphs:
	/// gabsIn		= SNOMAN absorption coefficients
	/// gabsRAT 	= RAT absorption MFPs directly converted from SNOMAN
	/// gRaymfp		= Rayleigh MFP
	/// gAbsmfp		= RAT absorption MFPs at output wavelengths
	/// gTotmfp		= combined absorption and scattering MFP
	/// gRayprob	= Probability of Rayleigh scattering per unit length
	/// gAbsprob	= probability of Absorption per unit length
	/// gfracray	= fraction of attenuation due to rayleigh
	/// gfracabs	= fraction of attenuation due to absorption
	/// gfractot	= cross-check sum of above 2 values
/// Output text:
	///	ABSLENGTH_value1
	/// ABSLENGTH_value2
	/// OPSCAT_FRAC_value1
	/// OPSCAT_FRAC_value2

/// Parameters:
	double lo_wave 			= 200;		// starting wavelength 
	double hi_wave 			= 800;		// last wavelength 
	const int nvals_output 	= 31;		// how many values do we want to output?
	bool verbose 			= false;	// output more info if true 
	double Confac 			= 1.53e26;	// Conversion factor used in SNOMAN (rayint_prob.for)
	double planks 			= 6.63e-34;	// Js
	double c 				= 3.00e8;	// m/s
	double MeV_J 			= 1.6e-13;	// MeV/J

	// Firstly plot the absorption coefficients we read in
	TGraph *gabsIn = new TGraph(ninp,wave,abscoeff);
	gabsIn->SetMarkerStyle(23);gabsIn->SetMarkerColor(3); gabsIn->SetLineColor(3);
	TCanvas *CabsA = new TCanvas("CabsA");
	CabsA->Divide(2,2);
	CabsA->cd(1);
	gabsIn->GetXaxis()->SetTitle("wavelength (nm)");
	gabsIn->GetYaxis()->SetTitle("(SNOMAN) Absorption coefficient (cm^{-1})");
	gabsIn->SetTitle("SNOMAN absorption coefficients");
	gabsIn->Draw("APL");
	
	// Now convert these to RAT format - absorption length in mm
	double abscoRAT[17];
	double waveRAT[17];
	// make sure we start with lo_wave (assume same value as start point)
	waveRAT[0] = lo_wave; 
	abscoRAT[0] = Attenuation(abscoeff[0]);
	for(int i=1; i<=ninp; ++i){
		abscoRAT[i] = Attenuation(abscoeff[i-1]);
		waveRAT[i]  = wave[i-1];
	}
	// add another entry on the end if it doesn't go all the way to hi_wave (same as last)
	waveRAT[ninp+1] = hi_wave;
	abscoRAT[ninp+1] = abscoRAT[ninp];
	TGraph *gabsRAT = new TGraph(ninp+2,waveRAT,abscoRAT);
	gabsRAT->SetMarkerStyle(23);gabsRAT->SetMarkerColor(3);gabsRAT->SetLineColor(3);
	gabsRAT->GetXaxis()->SetTitle("wavelength (nm)");
	gabsRAT->GetYaxis()->SetTitle("(RAT) Absorption length (mm)");
	gabsRAT->SetTitle("Mean Free Paths");
	CabsA->cd(2);
	gabsRAT->Draw("APL");

	// Choose more bins for the output format (will have to linearly interpolate input)
	double waveOut[nvals_output];		// Output wavelengths
	double rayprob[nvals_output];		// Probability of Rayleigh scattering per mm
	double absprob[nvals_output];		// Probability of absorption per mm
	double totprob[nvals_output];		// Probability of extinction per mm
	double mfp_ray[nvals_output];		// Rayleigh scattering mean free path (mm)
	double mfp_abs[nvals_output];		// Absorption mean free path with same sampling
	double mfp_tot[nvals_output];		// combined absorption and scattering
	double fracray[nvals_output];		// fraction due to Rayleigh
	double fracabs[nvals_output];		// fraction due to Absorption
	double fractot[nvals_output];		// just for a cross-check

	double RI2 = pow(meanRI,2);
	// Now calculate MFPs in mm and probabilities per mm for each component and combined
	for(int i=0; i<nvals_output; ++i){
		waveOut[i] = lo_wave + i*(hi_wave-lo_wave)/(nvals_output-1);
		// calculate Rayleigh
		double wl = 1e-9*waveOut[i];
		double energy = (planks*c)/(wl*MeV_J);
		rayprob[i] = 0.1 * Confac * isocomp * RSfactor * pow(energy,4.) *
				  pow((RI2-1.0),2.) * pow((RI2+2.0),2.);
		mfp_ray[i] = -1/(log(1-rayprob[i]));			
		// absorption
		mfp_abs[i] = gabsRAT->Eval(waveOut[i]);			
		absprob[i] = 1. - exp(-1./mfp_abs[i]);
		// combined
		mfp_tot[i] = 1./((1./mfp_abs[i]) + (1./mfp_ray[i]));
		totprob[i] = 1. - exp(-1./mfp_tot[i]);
		fracray[i] = rayprob[i]/totprob[i];
		fracabs[i] = absprob[i]/totprob[i];
		fractot[i] = fracray[i]+fracabs[i];
	}

	// Now plot everything - MFPs
	CabsA->cd(2);
	TGraph *gRaymfp = new TGraph(nvals_output,waveOut,mfp_ray);
	gRaymfp->SetTitle("Mean Free Paths");
	gRaymfp->SetMarkerStyle(21);gRaymfp->SetMarkerColor(2);gRaymfp->SetLineColor(2);
	gRaymfp->GetXaxis()->SetTitle("wavelength (nm)");
	gRaymfp->GetYaxis()->SetTitle("Mean free path (mm)");	
	gRaymfp->Draw("PL");
	TGraph *gAbsmfp = new TGraph(nvals_output,waveOut,mfp_abs);
	gAbsmfp->SetMarkerStyle(20);gAbsmfp->SetMarkerColor(4);gAbsmfp->SetLineColor(4);
	gAbsmfp->Draw("PL");
	TGraph *gTotmfp = new TGraph(nvals_output,waveOut,mfp_tot);
	gTotmfp->SetMarkerStyle(22);gTotmfp->SetMarkerColor(1);gTotmfp->SetLineColor(1);
	gTotmfp->Draw("PL");	
	// add a legend (keep marker coding same so that this will apply to all plots)
	TLegend *legAbsA = new TLegend(0.6,0.7,0.89,0.89);
	legAbsA->SetBorderSize(0);
	legAbsA->SetFillColor(0);
	legAbsA->AddEntry(gRaymfp,"Rayleigh","P");
	legAbsA->AddEntry(gAbsmfp,"Absorption","P");
	legAbsA->AddEntry(gTotmfp,"Total","P");
	legAbsA->Draw();
	// Now plot everything - probabilities
	CabsA->cd(3);
	TGraph *gRayprob = new TGraph(nvals_output,waveOut,rayprob);
	gRayprob->SetTitle("Probabilities");
	gRayprob->SetMarkerStyle(21);gRayprob->SetMarkerColor(2);gRayprob->SetLineColor(2);
	gRayprob->GetXaxis()->SetTitle("wavelength (nm)");
	gRayprob->GetYaxis()->SetTitle("probability per mm");	
	gRayprob->Draw("APL");
	TGraph *gAbsprob = new TGraph(nvals_output,waveOut,absprob);
	gAbsprob->SetMarkerStyle(20);gAbsprob->SetMarkerColor(4);gAbsprob->SetLineColor(4);
	gAbsprob->Draw("PL");
	TGraph *gTotprob = new TGraph(nvals_output,waveOut,totprob);
	gTotprob->SetMarkerStyle(22);gTotprob->SetMarkerColor(1);gTotprob->SetLineColor(1);
	gTotprob->Draw("PL");
	legAbsA->Draw();	
	// Now plot everything - fractions
	CabsA->cd(4);
	TGraph *gfracray = new TGraph(nvals_output,waveOut,fracray);
	gfracray->SetTitle("fractions");
	gfracray->SetMarkerStyle(21);gfracray->SetMarkerColor(2);gfracray->SetLineColor(2);
	gfracray->GetXaxis()->SetTitle("wavelength (nm)");
	gfracray->GetYaxis()->SetTitle("Fraction of total extinction");
	gfracray->Draw("APL");
	TGraph *gfracabs = new TGraph(nvals_output,waveOut,fracabs);
	gfracabs->SetMarkerStyle(20);gfracabs->SetMarkerColor(4);gfracabs->SetLineColor(4);
	gfracabs->Draw("PL");
	TGraph *gfractot = new TGraph(nvals_output,waveOut,fractot);
	gfractot->SetMarkerStyle(22);gfractot->SetMarkerColor(1);gfractot->SetLineColor(1);
	gfractot->Draw("PL");
	legAbsA->Draw();
	
	// Now to output the text in RAT format
	cout << "ABSLENGTH_option: \"wavelength\"," << endl;
	cout << "ABSLENGTH_value1: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(waveOut[i]) << ", ";	
	}
	cout << "], " << endl;				
    cout << "ABSLENGTH_value2: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(mfp_tot[i]) << ", ";
	}
	cout << "], " << endl;					
	cout << "OPSCATFRAC_option: \"wavelength\"," << endl;
	cout << "OPSCATFRAC_value1: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(waveOut[i]) << ", ";	
	}
	cout << "], " << endl;				
    cout << "OPSCATFRAC_value2: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(fracray[i]) << ", ";
	}
	cout << "], " << endl;					
}

///-----------------------------------------------------------------------------------------///
/// This method applies to scintillator materials where the absorption coefficients for
/// different components of the scintillator are specified by an array of 401 values in 
/// scintillator.dat (SCCO banks). The format in these banks is to specify 'a' for
/// wavelengths from 200nm to 600nm in 10nm steps, where I = Io.10^(-ax). For more than
/// one scintillator component, the absorption probabilities are combined using the
/// relative contribution values (a relative contribution > 1 means the absorption must
/// scaled up accordingly, eg if the measurement was made at lower concentration). They
/// are also combined with Rayleigh scattering (specified via a scale factor, a mean refractive
/// index and isothermal compressibility in media.dat) to obtain an overall extinction 
/// length, ABSLENGTH. The fraction of this extinction that is due to scattering is 
/// output as the OPSCATFRAC array. The wavelength dependent fraction that is due to 
/// each scintillator component is then used to combine the reemission probabilities for
/// each component to give the wavelength dependent REEMISSION_PROB.
void AbsScatRemScint(int nScintComp, double *relCont, double RSfactor, double meanRI, 
                     double isocomp, char *filenames[50], double *remprob){
/// Arguments:
	/// nScintComp 	= number of scintillator components
	/// relCont 	= pointer to double array of nScintComp values specifying relative
	///          	contribution of each scintillator component.
	/// RSfactor 	= Rayleigh Scattering scale factor from media.dat
	/// meanRI 		= mean refractive index for this material, taken from media.dat
	/// isocomp 	= Isothermal Compressibility of the material, taken from media.dat
	/// filenames 	= pointer to array of nScintComp filenames. Each file contains the 
	///				absorption coefficient data from the SCCO bank in scintillator.dat
	/// remprob		= pointer to double array of overall Reemission probability for each component
	
/// Output histograms and graphs:
	/// hsnoatt[nScintComp] = SNO attenuation coefficient
	/// hratabs[nScintComp] = RAT absorption MFPs
	/// gRaymfp				= Rayleigh MFP
	/// gAbsmfp				= RAT absorption MFPs at output wavelengths
	/// gTotmfp				= combined absorption and scattering MFP
	/// gTotprob			= combined absorption and scattering probability
	/// gRayprob			= Probability of Rayleigh scattering per unit length
	/// gAbsprob			= probability of Absorption per unit length
	/// gfracray			= fraction of attenuation due to rayleigh
	/// gfracabs			= fraction of attenuation due to absorption
	/// gfractot			= cross-check sum of above 2 values
	/// gremprob			= probability of reemission
	
	
/// Output text:
	///	ABSLENGTH_value1
	/// ABSLENGTH_value2
	/// OPSCAT_FRAC_value1
	/// OPSCAT_FRAC_value2
	/// REEMISSION_PROB_value1
	/// REEMISSION_PROB_value2

/// Parameters:
	int nvals_input         = 401;		// number of values in each input file
	double lo_wave 			= 200;		// starting wavelength 
	double hi_wave 			= 600;		// last wavelength 
	const int nvals_output 	= 40;		// how many values do we want to output?
	bool verbose 			= false;	// output more info if true 
	double Confac 			= 1.53e26;	// Conversion factor used in SNOMAN (rayint_prob.for)
	double planks 			= 6.63e-34;	// Js
	double c 				= 3.00e8;	// m/s
	double MeV_J 			= 1.6e-13;	// MeV/J
	const int MAX			= 4;		// maximum number of components
	double prob_unit;					// step size in mm
										
	// sort out the binning first
	int rb = int(nvals_input/nvals_output);		// combin rb bins into 1
	
	// loop through all the scintillator components and read data into histograms
	TH1D *hsnoatt[MAX];		// Store sno attenuation coefficient (cm^-1) we read in
	TH1D *hratabs[MAX];		// and store rat absorption length (mm)
	TCanvas *Cscintabs = new TCanvas("Cscintabs");	
	Cscintabs->Divide(2,2);
	TCanvas *Cremprob = new TCanvas("Cremprob");	
	if(nScintComp>MAX){
		// First check we don't have too many components
		cout << "Too many scintillator components" << endl;
		return;
	}
	for(int icomp = 0; icomp<nScintComp; ++icomp){
		hsnoatt[icomp] = 
		      new TH1D(Form("hsnoatt%d",icomp+1),"",int(hi_wave-lo_wave),lo_wave,hi_wave);
		hsnoatt[icomp]->SetLineColor(icomp+2);
		hsnoatt[icomp]->SetTitle("SNOMAN attenuation coefficients");
		hsnoatt[icomp]->SetXTitle("wavelength (nm)");
		hsnoatt[icomp]->SetYTitle("attenuation coefficient (cm^{-1})");
		hratabs[icomp] = 
		      new TH1D(Form("hratabs%d",icomp+1),"",int(hi_wave-lo_wave),lo_wave,hi_wave);
		hratabs[icomp]->SetLineColor(icomp+2);
		hratabs[icomp]->SetTitle("Mean Free Paths");
		hratabs[icomp]->SetXTitle("wavelength (nm)");
		hratabs[icomp]->SetYTitle("Mean Free Path (mm)");
		ifstream in;
		in.open(filenames[icomp]);
    	double val;
		int count = 0;
		while(1){
        	in >> val;
			hsnoatt[icomp]->SetBinContent(count,val);		// Store attenuation coefficient
			hratabs[icomp]->SetBinContent(count,Attenuation(val*relCont[icomp]*log(10)));	// Store absorption length
//bugfix - snoman values in base 10 not base e, and need to include relative contributions
//			hratabs[icomp]->SetBinContent(count,Attenuation(val));	// Store absorption length
    	 	if(!in.good())break;
			count++;
		}
		in.close();
		// Need to rebin the output histograms
		hratabs[icomp]->Rebin(rb);
		hratabs[icomp]->Scale(1/float(rb));
		if(verbose) cout << "Rebinning " << hratabs[icomp]->GetName() << " by " << rb << " -> " 
		                 << hratabs[icomp]->GetNbinsX() << " bins " << endl;
		Cscintabs->cd(1);
		gPad->SetLogy();
		if(icomp==0){
			hsnoatt[icomp]->Draw();
		}else{
			hsnoatt[icomp]->Draw("same");
		}
		Cscintabs->cd(2);
		gPad->SetLogy();
		if(icomp==0){
			hratabs[icomp]->Draw();
		}else{
			hratabs[icomp]->Draw("same");
		}
	}
	
	
	TLegend *legAbsB = new TLegend(0.52,0.5,0.82,0.62);
	legAbsB->SetBorderSize(0);
	legAbsB->SetFillColor(0);
	for(int icomp = 0; icomp<nScintComp; ++icomp){
		legAbsB->AddEntry(hratabs[icomp],Form("Scintillator Component - %d",icomp+1), "L");
	}
	Cscintabs->cd(1);
	legAbsB->Draw();
	Cscintabs->cd(2);
	legAbsB->Draw();
	
	// Now we need to combine these absorptions along with the rayleigh scattering
	double waveOut[nvals_output];		// Output wavelengths
	double rayprob[nvals_output];		// Probability of Rayleigh scattering per mm
	double absprob[nvals_output];		// Probability of absorption per mm
	double totprob[nvals_output];		// Probability of extinction per mm
	double mfp_ray[nvals_output];		// Rayleigh scattering mean free path (mm)
	double mfp_abs[nvals_output];		// Absorption mean free path with same sampling
	double mfp_tot[nvals_output];		// combined absorption and scattering
	double fracray[nvals_output];		// fraction due to Rayleigh
	double fracabs[nvals_output];		// fraction due to Absorption
	double fractot[nvals_output];		// just for a cross-check
	double absprobcomp[MAX][nvals_output];	// Probability of absorption per mm for sep components
	double absprobsum[nvals_output];	// Probability of absorption per mm for sep components
	double reemission[nvals_output];	// combine fraction absorbed by each component 
										// with o/a reemission for that component

	double RI2 = pow(meanRI,2);
	// Now calculate MFPs in mm and probabilities per mm for each component and combined
	for(int i=0; i<nvals_output; ++i){
		waveOut[i] = hratabs[0]->GetBinCenter(i+1);
		if(i==0)waveOut[i] = hratabs[0]->GetBinLowEdge(i+1);
		// calculate Rayleigh
		double wl = 1e-9*waveOut[i];
		double energy = (planks*c)/(wl*MeV_J);
		// probability of rayleigh defined per cm (convert to mm)
		rayprob[i] = 0.1 * Confac * isocomp * RSfactor * pow(energy,4.) *
				  pow((RI2-1.0),2.) * pow((RI2+2.0),2.);
		mfp_ray[i] = -1/(log(1.-rayprob[i]));	
		// absorption - sum over all components (by summing inverses of MFP)
		mfp_abs[i] = 0.;
		for(int icomp = 0; icomp<nScintComp; ++icomp){
			mfp_abs[i] += 1./hratabs[icomp]->GetBinContent(i+1);
		}
		mfp_abs[i] = 1./mfp_abs[i];
		// combined
		mfp_tot[i] = 1./((1./mfp_abs[i]) + (1./mfp_ray[i]));
		// use the total MFP to set the scale for the path-length for probabilities
		prob_unit = mfp_tot[i];
		totprob[i] = 1. - exp(-1.*prob_unit/mfp_tot[i]);
		rayprob[i] = 1. - exp(-1.*prob_unit/mfp_ray[i]);
		absprob[i] = 1. - exp(-1.*prob_unit/mfp_abs[i]);
		absprobsum[i] = 0.;
		for(int icomp = 0; icomp<nScintComp; ++icomp){
			absprobcomp[icomp][i] = 1. - exp(-1*prob_unit/(hratabs[icomp]->GetBinContent(i+1)));		
			absprobsum[i] += absprobcomp[icomp][i];		
		}
		// fractional contributions come from relative abs coeffs (ie inverse MFPs)
		fracray[i] = (1/mfp_ray[i])/(1/mfp_tot[i]);
		fracabs[i] = (1/mfp_abs[i])/(1/mfp_tot[i]);
		fractot[i] = fracray[i]+fracabs[i];
		// now deal with reemission
		reemission[i] = 0.;
		for(int icomp = 0; icomp<nScintComp; ++icomp){			
			reemission[i] += remprob[icomp]*((1./(hratabs[icomp]->GetBinContent(i+1)))/
			                 (1/mfp_abs[i]));	
		}
		
	}
	// Now plot everything - MFPs
	Cscintabs->cd(2);
	TGraph *gRaymfp = new TGraph(nvals_output,waveOut,mfp_ray);
	gRaymfp->SetMarkerStyle(21);gRaymfp->SetMarkerColor(4);gRaymfp->SetMarkerSize(0.5);gRaymfp->SetLineColor(4);
	gRaymfp->GetXaxis()->SetTitle("wavelength (nm)");
	gRaymfp->GetYaxis()->SetTitle("Mean free path (mm)");	
	gRaymfp->Draw("PL");
	TGraph *gAbsmfp = new TGraph(nvals_output,waveOut,mfp_abs);
	gAbsmfp->SetMarkerStyle(20);gAbsmfp->SetMarkerColor(6);gAbsmfp->SetMarkerSize(0.5);gAbsmfp->SetLineColor(6);
	gAbsmfp->Draw("PL");
	TGraph *gTotmfp = new TGraph(nvals_output,waveOut,mfp_tot);
	gTotmfp->SetMarkerStyle(22);gTotmfp->SetMarkerColor(1);gTotmfp->SetLineColor(1);
	gTotmfp->Draw("PL");	
	gTotmfp->SetName("gTotmfp");	
	gROOT->GetListOfSpecials()->Add(gTotmfp);
	// add a legend (keep marker coding same so that this will apply to all plots)
	TLegend *legAbsA = new TLegend(0.5,0.34,0.89,0.5);
	legAbsA->SetBorderSize(0);
	legAbsA->SetFillColor(0);
	legAbsA->AddEntry(gAbsmfp,"Combined Scintillator Absorption","P");
	legAbsA->AddEntry(gRaymfp,"Rayleigh","P");
	legAbsA->AddEntry(gTotmfp,"Total","P");
	legAbsA->Draw();
	// Now plot everything - probabilities
	Cscintabs->cd(3);
	TGraph *gRayprob = new TGraph(nvals_output,waveOut,rayprob);
	gRayprob->SetMarkerStyle(21);gRayprob->SetMarkerColor(4);gRayprob->SetMarkerSize(0.5);gRayprob->SetLineColor(4);
	gRayprob->SetTitle("Probabilities");
	gRayprob->GetXaxis()->SetTitle("wavelength (nm)");
	gRayprob->GetYaxis()->SetTitle("probability per total MFP");	
	gRayprob->Draw("APL");
	TGraph *gTotprob = new TGraph(nvals_output,waveOut,totprob);
	gTotprob->SetName("gTotprob");
	gROOT->GetListOfSpecials()->Add(gTotprob);
	gTotprob->SetMarkerStyle(22);gTotprob->SetMarkerColor(1);gTotprob->SetLineColor(1);
	gTotprob->Draw("PL");
	TGraph *gAbsprob = new TGraph(nvals_output,waveOut,absprob);
	gAbsprob->SetMarkerStyle(20);gAbsprob->SetMarkerColor(6);gAbsprob->SetMarkerSize(0.5);gAbsprob->SetLineColor(6);
	gAbsprob->Draw("PL");
	TGraph *gAbsprobcomp[MAX];
	for(int icomp=0; icomp<nScintComp; ++icomp){
		gAbsprobcomp[icomp] = new TGraph(nvals_output,waveOut,absprobcomp[icomp]);
		gAbsprobcomp[icomp]->SetLineColor(icomp+2);
		gAbsprobcomp[icomp]->Draw("L");
	}
	legAbsB->Draw();	
	legAbsA->Draw();	
	// Now plot everything - fractions
	Cscintabs->cd(4);
	TGraph *gfracray = new TGraph(nvals_output,waveOut,fracray);
	gfracray->SetName("gfracray");
	gROOT->GetListOfSpecials()->Add(gfracray);
	gfracray->SetTitle("Fractions");
	gfracray->SetMarkerStyle(21);gfracray->SetMarkerColor(4);gfracray->SetMarkerSize(0.8);gfracray->SetLineColor(4);
	gfracray->GetXaxis()->SetTitle("wavelength (nm)");
	gfracray->GetYaxis()->SetTitle("Fraction of total extinction");
	gfracray->Draw("APL");
	TGraph *gfracabs = new TGraph(nvals_output,waveOut,fracabs);
	gfracabs->SetMarkerStyle(20);gfracabs->SetMarkerColor(6);gfracabs->SetMarkerSize(0.5);gfracabs->SetLineColor(6);
	gfracabs->Draw("PL");
	TGraph *gfractot = new TGraph(nvals_output,waveOut,fractot);
	gfractot->SetMarkerStyle(22);gfractot->SetMarkerColor(1);gfractot->SetLineColor(1);
	gfractot->Draw("PL");
	legAbsA->Draw();
	// Now plot the reemission probability
	Cremprob->cd();
	TGraph *gremprob = new TGraph(nvals_output,waveOut,reemission);

gremprob->SetMarkerStyle(29);gremprob->SetMarkerColor(3);gremprob->SetMarkerSize(0.5);gremprob->SetLineColor(3);
	gremprob->SetName("gremprob");
	gROOT->GetListOfSpecials()->Add(gremprob);
	gremprob->SetTitle("Reemission probability");
	gremprob->GetXaxis()->SetTitle("wavelength (nm)");
	gremprob->GetYaxis()->SetTitle("probability of reemission");
	gremprob->Draw("APL");
	
	// Now to output the text in RAT format
	cout << "ABSLENGTH_option: \"wavelength\", " << endl;
	cout << "ABSLENGTH_value1: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(waveOut[i]) << ", ";	
	}
	cout << " 800.0d, ], " << endl;				
    cout << "ABSLENGTH_value2: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(mfp_tot[i]) << ", ";
	}
	cout << FormatRatD(mfp_tot[nvals_output-1]) << ", ], " << endl;					
    cout << "OPSCATFRAC_option: \"wavelength\", " << endl;
	cout << "OPSCATFRAC_value1: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(waveOut[i]) << ", ";	
	}
	cout << " 800.0d, ], " << endl;				
    cout << "OPSCATFRAC_value2: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(fracray[i]) << ", ";
	}
	cout << FormatRatD(fracray[nvals_output-1]) << ", ], " << endl;					
    cout << "REEMISSION_PROB_option: \"wavelength\", " << endl;
    cout << "REEMISSION_PROB_value1: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(waveOut[i]) << ", ";
	}
	cout << "800.0d, ], " << endl;					
    cout << "REEMISSION_PROB_value2: [";
	for(int i=0; i<nvals_output; ++i){
		cout << FormatRatD(reemission[i]) << ", ";
	}
	cout << FormatRatD(reemission[nvals_output-1])<< ", ], " << endl;					

}

///-----------------------------------------------------------------------------------------///
/// This method converts the array specifying the scintillation primary emission
/// spectrum in scintillator.dat (SCBU) into an array of intensity as a function of 
/// wavelength. The normalisation of intensity is nominally 1, but this is not used in 
/// RAT as long as a LIGHT_YIELD parameter, specifying the number of photons per MeV is 
/// also supplied. The input format is 200 entries: For the jth entry, the value Ntab, 
/// specifies that the probability of emission is j/NTAB. 
void ScintEmissionSpec(char filename[50]){
/// Arguments:
	/// filename 	= name of text file containing the input data in the SNOMAN format
	///				  specified above

/// Output text:
	/// SCINTILLATION_value1 	= array of wavelengths in nm
	/// SCINTILLATION_value2	= array of corresponding intensities (NOT cumulative).
	
/// Output histograms:
	TH1D *hscintIn;					// histogram of input data 
	TH1D *hscintOut;				// histogram of output data

/// Parameters:
    int nvals_input 	= 200;		// total number of input values
	double in_lo_wave 	= 200;		// starting wavelength 
	double in_hi_wave 	= 600;		// last wavelength 
	const int nvals_output 	= 40;	// how many values do we want to output?
	bool verbose 		= false;	// output more info if true 
	
	// open the input file
	ifstream in;
	in.open(filename);
    // create the necessary histograms
	int nbins = int(in_hi_wave-in_lo_wave);
	hscintIn    = new TH1D("hscintIn","",nbins,in_lo_wave,in_hi_wave);
	hscintIn->SetTitle("Input Scintillator Primary Emission Spectrum");
	hscintIn->SetXTitle("wavelength (nm)");
	hscintIn->SetYTitle("primary emission intensity");
    hscintOut   = new TH1D("hscintOut","",nbins,in_lo_wave,in_hi_wave);
	hscintOut->SetTitle("Output Scintillator Primary Emission Spectrum");
	hscintOut->SetXTitle("wavelength (nm)");
	hscintOut->SetYTitle("primary emission intensity (normalised to 1)");	
    hscintSample   = new TH1D("hscintSample","",400,200.,600.);
	
	int count = 0;					// keep check of how many values input
	int lastbin = 0;				// and remember what last bin added was
	double norm = 0;
	double val;						// store to temporary value
	while (1){
        in >> val;
        int bin = hscintIn->FindBin(val);
        hscintIn->SetBinContent(bin,count+1);
        norm =+count;
        if(lastbin != 0){
            for(int j=lastbin; j<bin; ++j){
				// need to set all the bins inbetween to the same value
                hscintIn->SetBinContent(j,count);
                norm =+count;                   
            }
    	}
    	if(!in.good())break;
        lastbin = bin;
		count++;
	}
	hscintIn->Scale(1./norm);
	in.close();
	
	if(verbose)cout << "Input " << count << " values" << endl;
	// Draw the input spectrum
	TCanvas *Cscint = new TCanvas("Cscint");	// firstly we need a canvas
	Cscint->Divide(1,2);
	Cscint->cd(1);
	hscintIn->Draw();
	
	// An alternative way to produce the output spectrum is to sample - check against the code in snoman.
	for(int i=0; i<1e6; ++i){
		float ran = gRandom->Uniform();
		int ibin = 1;
		while(hscintIn->GetBinContent(ibin)<ran){
			ibin++;
		}
		// now need to interpolate bin
        int space = 1;
		while( hscintIn->GetBinContent(ibin)==hscintIn->GetBinContent(ibin+space)
		       && (ibin+space)<hscintIn->GetNbinsX()){
			space++;
		}	
		float w = hscintIn->GetBinCenter(ibin) + space*gRandom->Uniform()*hscintIn->GetBinWidth(ibin+1);		
		hscintSample->Fill(w);
//		cout << ran << " " << ibin << " " << w << " " << hscintIn->GetBinContent(ibin) << endl;
	}
	hscintSample->Scale(1./float(hscintSample->GetEntries()));
	
    // Now convert to absolute not cumulative values	
    double last = 0;				// Store value from last bin since its cumulative
	for(int ibin = 1; ibin<=nbins; ++ibin){
    	val = hscintIn->GetBinContent(ibin);
    	hscintOut->SetBinContent(ibin,(val-last));
    	last = val;
    }
	// And rebin the histogram 
	int rb = int(nbins/nvals_output);		// combin rb bins into 1
    hscintOut->Rebin(rb);
	if(verbose)cout << "Rebinning by " << rb << " -> " << hscintOut->GetNbinsX() << " output bins " << endl;
    hscintOut->Scale(double(1./rb));			// preserve normalisation
	// And draw the output histogram
	Cscint->cd(2);
    hscintOut->Draw();
    hscintSample->SetLineColor(2);
	hscintSample->Draw("same");
	
	// Now to output the text in RAT format
	cout << "SCINTILLATION_option: \"dy_dwavelength\", " << endl ;
	cout << "SCINTILLATION_value1: [";
	double wave[nvals_output];
	for(int i=0; i<nvals_output; ++i){
		wave[i] = hscintOut->GetBinCenter(i+1);
		if(i==0) wave[i] = hscintOut->GetBinLowEdge(i+1);
		cout << FormatRatD(wave[i]) << ", ";	
	}
	cout << "800d, ], " << endl;				// want data to go up to 800nm 
    cout << "SCINTILLATION_value2: [";
	for(int i=0; i<nvals_output; ++i){
		val = hscintOut->GetBinContent(i+1);
		cout << FormatRatD(val) << ", ";
	}
	cout << "0d, ], " << endl;				// set intensity at 800nm to be 0.	

}

///-----------------------------------------------------------------------------------------///
/// This method converts the array specifying the reemission spectrum in
/// scintillator.dat (SCCO) into an array of intensity as a function of wavelength. At
/// present we assume that there is only one reemission spectrum, even for a
/// multi-component scintillator. The normalisation of output intensity is nominally 1, 
/// but only the shape is considered in RAT anyway. The input format is 401 values
/// specifying the cumulative emission probability from 200-600nm in 10nm steps.
void ScintReemissionSpec(char filename[50]){
/// Arguments:
	/// filename 	= name of text file containing the input data in the SNOMAN format
	///				  specified above

/// Output text:
	/// SCINTILLATION_WLS_value1 	= array of wavelengths in nm
	/// SCINTILLATION_WLS_value2	= array of corresponding intensities (NOT cumulative).
	
/// Output histograms:
	TH1D *hremIn;					// histogram of input data 
	TH1D *hremOut;					// histogram of output data

/// Parameters:
    int nvals_input 	= 400;		// total number of input values
	double in_lo_wave 	= 200;		// starting wavelength input
	double in_hi_wave 	= 600;		// last wavelength input
	const int nvals_output 	= 40;	// how many values do we want to output?
	bool verbose 		= false;	// output more info if true 
	
	// open the input file
	ifstream in;
	in.open(filename);
    // create the necessary histograms
	hremIn    = new TH1D("hremIn","",nvals_input,in_lo_wave,in_hi_wave);
	hremIn->SetTitle("Input Cumulative Reemission Spectrum");
	hremIn->SetXTitle("wavelength (nm)");
	hremIn->SetYTitle("cumulative remission intensity");
    hremOut   = new TH1D("hremOut","",nvals_input,in_lo_wave,in_hi_wave);
	hremOut->SetTitle("Output Differential Reemission Spectrum");
	hremOut->SetXTitle("wavelength (nm)");
	hremOut->SetYTitle("reemission intensity (normalised to 1)");	
	
	int count = 0;					// keep check of how many values input
	double val;						// store to temporary value
	while (1){
        in >> val;
		hremIn->SetBinContent(count+1,val);
    	if(!in.good())break;
		count++;
	}
	in.close(); 
	
	if(verbose)cout << "Input " << count << " values" << endl;
	// Draw the input spectrum
	TCanvas *Crem = new TCanvas("Crem");	// firstly we need a canvas
	Crem->Divide(1,2);
	Crem->cd(1);
	hremIn->Draw();
	
    // Now convert to absolute not cumulative values	
    double last = 0;				// Store value from last bin since its cumulative
	for(int ibin = 1; ibin<=nvals_input; ++ibin){
    	val = hremIn->GetBinContent(ibin);
    	hremOut->SetBinContent(ibin,(val-last));
    	last = val;
    }
	// And rebin the histogram 
	int rb = int(nvals_input/nvals_output);		// combin rb bins into 1
    hremOut->Rebin(rb);
	if(verbose)cout << "Rebinning by " << rb << " -> " << hremOut->GetNbinsX() << " output bins " << endl;
    hremOut->Scale(double(1./rb));			// preserve normalisation
	// And draw the output histogram
	Crem->cd(2);
    hremOut->Draw();
    
	// Now to output the text in RAT format
	cout << "SCINTILLATION_WLS_option: \"dy_dwavelength\", " << endl ;
	cout << "SCINTILLATION_WLS_value1: [";
	double wave[nvals_output];
	for(int i=0; i<nvals_output; ++i){
		wave[i] = hremOut->GetBinCenter(i+1);
		if(i==0) wave[i] = hremOut->GetBinLowEdge(i+1);
		cout << FormatRatD(wave[i]) << ", ";	
	}
	cout << "800d, ], " << endl;				// want data to go up to 800nm 
    cout << "SCINTILLATION_WLS_value2: [";
	for(int i=0; i<nvals_output; ++i){
		val = hremOut->GetBinContent(i+1);
		cout << FormatRatD(val) << ", ";
	}
	cout << "0d, ], " << endl;				// set intensity at 800nm to be 0.	

}

///-----------------------------------------------------------------------------------------///
/// Helper method to reformat a string into ratdb double output format
string FormatRatD(double val){
	stringstream ss;
	ss << val;
	string sratd;
	ss >> sratd;
	/// if number is in scientific format - replace e with d, else just add a d on the end
	size_t found = sratd.find("e");
	if(found!=string::npos){
		sratd.replace(sratd.find("e"),1,"d");			
	}else{
		sratd.append("d");
	}	
	return sratd;
}

///-----------------------------------------------------------------------------------------///
/// Convert the attenuation coefficients in SNOMAN (media.dat) to absorption lengths in RAT 
/// format ABSLENGTH. 
/// In SNOMAN have attenuation coeff a, defined by   I = Io.exp(-ax)	 where a in cm-1
/// In RAT have absorption length, A defined by      I = Io.exp(-x/A) 	 where A in mm
double Attenuation(double value){
	return 10./value;
}

///-----------------------------------------------------------------------------------------///


