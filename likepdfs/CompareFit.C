/*-----------------------------------------------------------------------
/// This program compares fitted and generated event positions and energies 
/// for single particle events. Plot trends for dX, dY,dZ, dE for each position fitter  
/// (Centroid, QPDF, FitLike)
/// and dE for each energy fitter
/// (FitLike)

/// To run, open root, and type:
/// > .L CompareFit.C
/// > CompareFit("filename")
/// where "filename" is the name of the RAT root output file. 
-----------------------------------------------------------------------*/
void CompareFit( char *lpFile )
{
	/// Only consider events inside this fiducial volume
	float fidvol = 5500.;
	TFile *file = new TFile(lpFile);
	TTree *tree = file->Get("T");
	RAT::DS::Root *rds = new RAT::DS::Root();

	tree->SetBranchAddress("ds", &rds);

	/// Set up histograms to store results of different fitters
	/// Centroid fitter
	TH1D *hxdCen= new TH1D("hxdCen","Delta X",1000,-1000,1000);
	TH1D *hydCen= new TH1D("hydCen","Delta Y",1000,-1000,1000);
	TH1D *hzdCen= new TH1D("hzdCen","Delta Z",1000,-1000,1000);
	TH1D *hrdCen= new TH1D("hrdCen","Delta R",400,0,400);
	hxdCen->SetLineColor(1);
	hydCen->SetLineColor(1);
	hzdCen->SetLineColor(1);
	hrdCen->SetLineColor(1);

	/// QPDF fitter
	TH1D *hxdQPDF= new TH1D("hxdQPDF","Delta X",1000,-1000,1000);
	TH1D *hydQPDF= new TH1D("hydQPDF","Delta Y",1000,-1000,1000);
	TH1D *hzdQPDF= new TH1D("hzdQPDF","Delta Z",1000,-1000,1000);
	TH1D *hrdQPDF= new TH1D("hrdQPDF","Delta R",400,0,400);
	hxdQPDF->SetLineColor(3);
	hydQPDF->SetLineColor(3);
	hzdQPDF->SetLineColor(3);
	hrdQPDF->SetLineColor(3);

	/// Likelihood fitter - position
	TH1D *hxdLike= new TH1D("hxdLike","",1000,-1000,1000);
	hxdLike->SetXTitle("X - Xfit (mm)");
	TH1D *hydLike= new TH1D("hydLike","",1000,-1000,1000);
	hydLike->SetXTitle("Y - Yfit (mm)");
	TH1D *hzdLike= new TH1D("hzdLike","",1000,-1000,1000);
	hzdLike->SetXTitle("Z - Zfit (mm)");
	TH1D *hrdLike= new TH1D("hrdLike","",400,0,400);
	hxdLike->SetLineColor(4);
	hydLike->SetLineColor(4);
	hzdLike->SetLineColor(4);
	hrdLike->SetLineColor(4);

	/// Likelihood fitter - energy
	hrdLike->SetXTitle("\DeltaRfit (mm)");
	TH1D *hedLike= new TH1D("hedLike","",1000,-20,20);
	hedLike->SetXTitle("(E - Efit)/E (\%)");
	hedLike->SetLineColor(4);

	Int_t iNoEvents = tree->GetEntries();   
	/// For first 500 events, keep an eye on any bad fits by the likelihood fitter
	const int NN = 500;
	double xtrue[NN], ytrue[NN], ztrue[NN], xdiff[NN], ydiff[NN], zdiff[NN];
	double rtrue[NN], rdiff[NN], fom[NN];
	for(int ii=0; ii<NN; ++ii){
		xtrue[ii] =6000; ytrue[ii]=6000; ztrue[ii]=6000; rtrue[ii]=6000;
		xdiff[ii] =0; ydiff[ii]=0; zdiff[ii]=0; rdiff[ii]=0;
		fom[ii] =0;
	}
	int ngood = 0;
	int nbad  = 0;

	for(int iLoop=0; iLoop<iNoEvents; iLoop++ ){
        tree->GetEntry( iLoop );  
		
		/// Get the true event position from the MC branch 
        RAT::DS::MC *rmc = rds->GetMC();
        RAT::DS::MCParticle *rmcparticle =  rmc->GetMCParticle(0);
		/// Only consider events inside the fiducial volume
		if(pow((pow(rmcparticle->GetPosition().x(),2)+ pow(rmcparticle->GetPosition().y(),2)
			+pow(rmcparticle->GetPosition().z(),2)),0.5)>fidvol)continue;
        if( rds->GetEVCount() == 0 ) continue;
		if(iLoop<NN){
			xtrue[iLoop] = rmcparticle->GetPosition().x();
			ytrue[iLoop] = rmcparticle->GetPosition().y();
			ztrue[iLoop] = rmcparticle->GetPosition().z();
			rtrue[iLoop] = pow((pow(xtrue[iLoop],2)+pow(ytrue[iLoop],2)+pow(ztrue[iLoop],2)),0.5);
        }
		RAT::DS::EV *rev = rds->GetEV(0);

        RAT::DS::PosFit *rposfit;

		/// Loop through all fitters applied
  		for(int iLoop2=0; iLoop2 < rev->GetPosFitCount(); iLoop2++ ){
			rposfit =  rev->GetPosFit( iLoop2 ); 
			string fitname = rposfit->GetFitName();
			Double_t fDeltaX = rmcparticle->GetPosition().x() - rposfit->GetPosition().x();
			Double_t fDeltaY = rmcparticle->GetPosition().y() - rposfit->GetPosition().y();
			Double_t fDeltaZ = rmcparticle->GetPosition().z() - rposfit->GetPosition().z();
	   		Double_t fDeltaR = pow( pow( fDeltaX, 2 ) + pow( fDeltaY, 2 ) + pow( fDeltaZ, 2 ), 0.5);
			
			// which histograms to put things in 
			if(fitname.compare("centroid")==0){
				hxdCen->Fill(fDeltaX);
				hydCen->Fill(fDeltaY);
				hzdCen->Fill(fDeltaZ);
				hrdCen->Fill(fDeltaR);
			}else if(fitname.compare("QPDFitter")==0){
				hxdQPDF->Fill(fDeltaX);
				hydQPDF->Fill(fDeltaY);
				hzdQPDF->Fill(fDeltaZ);
				hrdQPDF->Fill(fDeltaR);
			}else if(fitname.compare("fitlikepos")==0){
				if(iLoop<NN){
					xdiff[iLoop] = fDeltaX;
					ydiff[iLoop] = fDeltaY;
					zdiff[iLoop] = fDeltaZ;
					rdiff[iLoop] = fDeltaR;
					/// define a bad fit as >4m off!
					if(rdiff[iLoop]>400){
				 		if(verbose){
							cout << iLoop << " (" 
								 << xtrue[iLoop] << ", " 
								 << ytrue[iLoop] << ", " 
								 << ztrue[iLoop] << ") " 
								 << rtrue[iLoop] << " :  (" 
								 << xdiff[iLoop]  << ", " 
								 << ydiff[iLoop]  << ", " 
								 << zdiff[iLoop]  << ") " 
								 << rdiff[iLoop] <<endl;
						}
						nbad++;	 	
					}else{
						ngood++;
						hxdLike->Fill(fDeltaX);
						hydLike->Fill(fDeltaY);
						hzdLike->Fill(fDeltaZ);
						hrdLike->Fill(fDeltaR);
					}
				}	
			}
        }
		Double_t fEnergy;
        RAT::DS::EFit *refit;
        for(int iLoop2=0; iLoop2<rev->GetEFitCount(); iLoop2++ )
        {
			refit =  rev->GetEFit( iLoop2 ); 
            Double_t fDeltaE = 100*(rmcparticle->GetKE() - refit->GetKE())/
                                                rmcparticle->GetKE();
    		string fitname = refit->GetFitName();
    		if(fitname.compare("fitlikeenergy")==0){
            	hedLike->Fill(fDeltaE);
				if(rdiff[iLoop]>400){
					cout << fDeltaE << endl;
				}	
    		}
		}		
	}
	if(nbad>0) cout << ngood << " good Like fits, " << nbad << " Bad Like Fits " << endl;

	// Now draw
	TCanvas *C1 = new TCanvas("C1");
	C1->Divide(2,2);
	C1->cd(1);
	hxdLike->Draw();
	hxdChi->Draw("same");
	hxdCen->Draw("same");
	hxdQPDF->Draw("same");
	C1->cd(2);
	hydLike->Draw();
	hydChi->Draw("same");
	hydCen->Draw("same");
	hydQPDF->Draw("same");
	C1->cd(3);
	hzdLike->Draw();
	hzdChi->Draw("same");
	hzdCen->Draw("same");
	hzdQPDF->Draw("same");
	C1->cd(4);
	hrdLike->Draw();
	hrdChi->Draw("same");
	hrdCen->Draw("same");
	hrdQPDF->Draw("same");
	TCanvas *C2 = new TCanvas("C2");
	hedLike->Draw();

	TCanvas *C3 = new TCanvas("C3");
	TPad *p1 = new TPad("p1","X fit",0,   0.5, 0.33, 1.0, 0,0,0);	
	TPad *p2 = new TPad("p2","Y fit",0.33,0.5, 0.66, 1.0, 0,0,0);	
	TPad *p3 = new TPad("p3","Z fit",0.66,0.5, 1.0,  1.0, 0,0,0);	
	TPad *p4 = new TPad("p4","E fit",0,   0.0, 0.5,  0.5, 0,0,0);
	TPad *p5 = new TPad("p5","R fit",0.5, 0,   1.0,  0.5, 0,0,0);	
	p1->Draw();
	p2->Draw();
	p3->Draw();
	p4->Draw();
	p5->Draw();
	p1->cd();
	hxdLike->Draw();
	p2->cd();
	hydLike->Draw();
	p3->cd();
	hzdLike->Draw();
	p4->cd();
    hedLike->Draw();
    p5->cd();	hrdLike->Draw();
	// Now output results - in format suitable for Latex table
	printf("%s & %5.2f  & %5.2f & %5.2f & %5.2f & %5.2f & %5.2f & %5.2f & %5.2f & %5.2f  \\\\ \n",
		lpFile,
		hxdLike->GetMean(),hxdLike->GetRMS(),
		hydLike->GetMean(),hydLike->GetRMS(),
		hzdLike->GetMean(),hzdLike->GetRMS(),
        hedLike->GetMean(),hedLike->GetRMS(),
		hrdLike->GetMean());
		
	TCanvas *C4 = new TCanvas("C4");
	C4->cd();
	// try plotting difference against true parameter - this shows where fit fails	
	TGraph *gxLike = new TGraph(NN,xtrue,xdiff);
	TGraph *gyLike = new TGraph(NN,ytrue,ydiff);
	TGraph *gzLike = new TGraph(NN,ztrue,zdiff);
	TGraph *grLike = new TGraph(NN,rtrue,rdiff);
	gxLike->SetMarkerStyle(7);
	gyLike->SetMarkerStyle(7);
	gzLike->SetMarkerStyle(7);
	grLike->SetMarkerStyle(7);
	TPad *pp1 = new TPad("pp1","X fit",0,   0.5, 0.33, 1.0, 0,0,0);	
	TPad *pp2 = new TPad("pp2","Y fit",0.33,0.5, 0.66, 1.0, 0,0,0);	
	TPad *pp3 = new TPad("pp3","Z fit",0.66,0.5, 1.0,  1.0, 0,0,0);	
	TPad *pp4 = new TPad("pp4","R fit",0.0, 0,   1.0,  0.5, 0,0,0);	
	pp1->Draw();
	pp2->Draw();
	pp3->Draw();
	pp4->Draw();
	pp1->cd();
	gxLike->Draw("AP");
	pp2->cd();
	gyLike->Draw("AP");
	pp3->cd();
	gzLike->Draw("AP");
	pp4->cd();
	grLike->Draw("AP");
		
}
