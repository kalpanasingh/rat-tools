void Run(char* option){

	gROOT->ProcessLine(".L Optics_SNOMAN_to_RAT.C");
	SetUp();

	if(option == "h2o"){
		// lightwater_sno refractive index
		double RI_h2o[3] = {1.302, 0.01562, 0.32 };
		RefIndex(RI_h2o);
		// lightwater_sno absorption and scattering (from make_scintillator cmdfiles)
		double meanRI_h2o = 1.342;
		double RSf_h2o = 0.87;
		double isocomp_h2o = 4.78e-10;
		double wave_h2o[6] = {337.0, 365.0, 386.0, 420.0, 500.0, 620.0};
		double absco_h2o[6] = {4.949e-05, 2.407e-05, 1.226e-04, 3.071e-04, 5.766e-04, 2.183e-03};
		AbsScatNonScint(6, wave_h2o, absco_h2o, RSf_h2o, meanRI_h2o, isocomp_h2o);
	}
	
	if(option == "d2o"){	
		// heavywater_sno refractive index
		double RI_d2o[3] = {1.302, 0.01333, 0.32};
		RefIndex(RI_d2o);
		// D2O absorption and scattering (from media_qoca_jan22)
		double meanRI_d2o = 1.337;
		double RSf_d2o = 2.0;
		double isocomp_d2o = 4.92e-10; 
		double wave_d2o[6] = {337.0, 365.0, 386.0, 420.0, 500.0, 620.0};
		double absco_d2o[6] = {1.697e-05, 5.450e-05, 5.962e-05, 4.851e-05, 3.760e-05, 4.236e-05};
		AbsScatNonScint(6, wave_d2o, absco_d2o, RSf_d2o, meanRI_d2o, isocomp_d2o);
	}
	
	if(option == "acrylic"){	
		// acrylic_sno refractive index
		double RI_acrylic[3] = {1.452, 0.02, 0.32 };
		RefIndex(RI_acrylic);
		// acrylic absorption and scattering (from make_scintillator cmdfile)
		double meanRI_acr = 1.5;
		double RSf_acr = 0.95;
		double isocomp_acr = 3.55e-10; 
		double wave_acr[6] = {337.0, 365.0, 386.0, 420.0, 500.0, 620.0};
		double absco_acr[6] = {5.610e-02, 2.279e-02, 1.204e-02, 7.587e-03, 7.036e-03, 7.068e-03};
		AbsScatNonScint(6, wave_acr, absco_acr, RSf_acr, meanRI_acr, isocomp_acr);	
	}
	
	if(option == "glass"){
		// glass_sno refractive index
		double RI_glass[3] = {1.458, 0.0, 0.0 };
		RefIndex(RI_glass);	
	}

	if(option == "pcppo"){
		// pcppo_scintillator refractive index
		double RI_pcppo[3] = {1.505, 0.0, 0.0 };
		RefIndex(RI_pcppo);
		// PCPPO primary emission
		ScintEmissionSpec("text_files/PCPPO_primaryemission.txt");
		// PCPPO reemission
		ScintReemissionSpec("text_files/PCPPO_reemission.txt");
		// PCPPO absorption and scattering
		char *filenames_pcppo[1];
		filenames_pcppo[0] = "text_files/PCPPO_absorption.txt";
		double relCont_pcppo[2] = {1.0}; 
		double remprob_pcppo[2] = {0.8};
		double RSf_pcppo = 12.14;
		double RImean_pcppo = 1.505;
		double isocomp_pcppo = 4.92e-10;
		AbsScatRemScint(1, relCont_pcppo, RSf_pcppo, RImean_pcppo, isocomp_pcppo,
		                filenames_pcppo, remprob_pcppo);

		// Now make a comparison plot (and rename histograms)
		// rerun the last with a different unit to show details at higher wavelengths
		TH1F *hpcppo_prim = (TH1F*)hscintOut->Clone("hpcppo_prim");
		hpcppo_prim->Scale(50);
		hpcppo_prim->SetAxisRange(0.,1.1,"Y");
		hpcppo_prim->SetYTitle("");
		hpcppo_prim->SetTitle("");
		TH1F *hpcppo_reem = (TH1F*)hremOut->Clone("hpcppo_reem");
		hpcppo_reem->Scale(50);
		hpcppo_reem->SetLineColor(2);
		TGraph *gpcppo_mfp = (TGraph*)gROOT->FindObject("gTotmfp");
		gpcppo_mfp->SetName("gpcppo_mfp");
		TGraph *gpcppo_opscat  = (TGraph*)gROOT->FindObject("gfracray");
		gpcppo_opscat->SetName("gpcppo_opscat");
		TGraph *gpcppo_remprob = (TGraph*)gROOT->FindObject("gremprob");
		gpcppo_remprob->SetName("gpcppo_remprob"); 
		TCanvas *CanCom = new TCanvas("CanCom");
		CanCom->cd();
		hpcppo_prim->Draw();
		hpcppo_reem->Draw("same");
		gpcppo_mfp->Draw("PL");
		gpcppo_opscat->Draw("PL");
		gpcppo_remprob->Draw("PL");
		TLegend *legCom = new TLegend(0.55,0.28,0.89,0.53);
		legCom->SetBorderSize(0);
		legCom->SetFillColor(0);
		legCom->AddEntry(hpcppo_prim,"Primary Emission Spectrum", "L");
		legCom->AddEntry(hpcppo_reem,"Reemission Spectrum", "L");
		legCom->AddEntry(gpcppo_mfp,"Total MFP for extinction in mm", "PL");
		legCom->AddEntry(gpcppo_opscat,"Fraction of Attenuation due to Rayleigh", "PL");
		legCom->AddEntry(gpcppo_remprob,"Probability of Reemission if absorbed","PL");
		legCom->Draw();
		
/*		
		// could output the plots to file here if you want
		TFile g("pcppo_plots.root","RECREATE");
		g.Append(hpcppo_prim);execute c++
		g.Append(hpcppo_reem);
		g.Append(gpcppo_mfp);
		g.Append(gpcppo_opscat);
		g.Append(gpcppo_remprob);
		g.Write();
*/
	}	
	
	if(option == "labppo"){
		// labppo_scintillator refractive index
		double RI_labppo[3] = {1.505, 0.0, 0.0 };
		RefIndex(RI_labppo);
		// LABPPO primary emission
		ScintEmissionSpec("text_files/LABPPO_primary_emission.txt");
		// LABPPO remission
		ScintReemissionSpec("text_files/PPO_reemission.txt");
		// LABPPO absorption and scattering
		char *filenames_labppo[2];
		filenames_labppo[0] = "text_files/LAB_absorption.txt";
		filenames_labppo[1] = "text_files/PPO_absorption.txt";
		double relCont_labppo[2] = {1.0,0.001}; 
		double remprob_labppo[2] = {0.0001,0.8};
		double RSf_labppo = 12.14;
		double RImean_labppo = 1.505;
		double isocomp_labppo = 4.92e-10;
		AbsScatRemScint(2, relCont_labppo, RSf_labppo, RImean_labppo, isocomp_labppo,
		                filenames_labppo, remprob_labppo);

		// Now make a comparison plot (and rename histograms)
		TH1F *hlabppo_prim = (TH1F*)hscintOut->Clone("hlabppo_prim");
		hlabppo_prim->Scale(50);
		hlabppo_prim->SetAxisRange(0.,1.1,"Y");
		hlabppo_prim->SetYTitle("");
		hlabppo_prim->SetTitle("");
		TH1F *hlabppo_reem = (TH1F*)hremOut->Clone("hlabppo_reem");
		hlabppo_reem->Scale(50);
		hlabppo_reem->SetLineColor(2);
		TGraph *glabppo_mfp = (TGraph*)gROOT->FindObject("gTotmfp");
		glabppo_mfp->SetName("glabppo_mfp");
		TGraph *glabppo_opscat  = (TGraph*)gROOT->FindObject("gfracray");
		glabppo_opscat->SetName("glabppo_opscat");
		TGraph *glabppo_remprob = (TGraph*)gROOT->FindObject("gremprob");
		glabppo_remprob->SetName("glabppo_remprob");
		TCanvas *CanCom = new TCanvas("CanCom");
		CanCom->cd();
		hlabppo_prim->Draw();
		hlabppo_reem->Draw("same");
		glabppo_mfp->Draw("PL");
		glabppo_opscat->Draw("PL");
		glabppo_remprob->Draw("PL");
		TLegend *legCom = new TLegend(0.55,0.28,0.89,0.53);
		legCom->SetBorderSize(0);
		legCom->SetFillColor(0);
		legCom->AddEntry(hlabppo_prim,"Primary Emission Spectrum", "L");
		legCom->AddEntry(hlabppo_reem,"Reemission Spectrum", "L");
		legCom->AddEntry(glabppo_mfp,"Total MFP for extinction in mm", "PL");
		legCom->AddEntry(glabppo_opscat,"Fraction of Attenuation due to Rayleigh", "PL");
		legCom->AddEntry(glabppo_remprob,"Probability of Reemission if absorbed","PL");
		legCom->Draw();
		
/*
		// could output the plots to file here if you want
		TFile f("labppo_plots.root","RECREATE");
		f.Append(hlabppo_prim);
		f.Append(hlabppo_reem);
		f.Append(glabppo_mfp);
		f.Append(glabppo_opscat);
		f.Append(glabppo_remprob);
		f.Write();
*/
	}	


if(option == "ndlabppo_noscatt_noabs"){
		// labppo_scintillator refractive index
		double RI_labppo[3] = {1.505, 0.0, 0.0 };
		RefIndex(RI_labppo);
		// LABPPO primary emission
		ScintEmissionSpec("text_files/LABPPO_primary_emission.txt");
		// LABPPO remission
		ScintReemissionSpec("text_files/PPO_reemission.txt");
		// LABPPO absorption and scattering
		char *filenames_labppo[3];
		filenames_labppo[0] = "text_files/no_absorption.txt";
		filenames_labppo[1] = "text_files/no_absorption.txt";	
		filenames_labppo[2] = "text_files/no_absorption.txt";
		double relCont_labppo[3] = {0.99829, 0.001710,0.0001}; 
		double remprob_labppo[3] = {0.0001,0.8,0.0};
		double RSf_labppo = 0.000001;
		double RImean_labppo = 1.505;
		double isocomp_labppo = 4.92e-10;
		AbsScatRemScint(3, relCont_labppo, RSf_labppo, RImean_labppo, isocomp_labppo,
		                filenames_labppo, remprob_labppo);

		// Now make a comparison plot (and rename histograms)
		TH1F *hlabppo_prim = (TH1F*)hscintOut->Clone("hlabppo_prim");
		hlabppo_prim->Scale(50);
		hlabppo_prim->SetAxisRange(0.,1.1,"Y");
		hlabppo_prim->SetYTitle("");
		hlabppo_prim->SetTitle("");
		TH1F *hlabppo_reem = (TH1F*)hremOut->Clone("hlabppo_reem");
		hlabppo_reem->Scale(50);
		hlabppo_reem->SetLineColor(2);
		TGraph *glabppo_mfp = (TGraph*)gROOT->FindObject("gTotmfp");
		glabppo_mfp->SetName("glabppo_mfp");
		TGraph *glabppo_opscat  = (TGraph*)gROOT->FindObject("gfracray");
		glabppo_opscat->SetName("glabppo_opscat");
		TGraph *glabppo_remprob = (TGraph*)gROOT->FindObject("gremprob");
		glabppo_remprob->SetName("glabppo_remprob");
		TCanvas *CanCom = new TCanvas("CanCom");
		CanCom->cd();
		hlabppo_prim->Draw();
		hlabppo_reem->Draw("same");
		glabppo_mfp->Draw("PL");
		glabppo_opscat->Draw("PL");
		glabppo_remprob->Draw("PL");
		TLegend *legCom = new TLegend(0.55,0.28,0.89,0.53);
		legCom->SetBorderSize(0);
		legCom->SetFillColor(0);
		legCom->AddEntry(hlabppo_prim,"Primary Emission Spectrum", "L");
		legCom->AddEntry(hlabppo_reem,"Reemission Spectrum", "L");
		legCom->AddEntry(glabppo_mfp,"Total MFP for extinction in mm", "PL");
		legCom->AddEntry(glabppo_opscat,"Fraction of Attenuation due to Rayleigh", "PL");
		legCom->AddEntry(glabppo_remprob,"Probability of Reemission if absorbed","PL");
		legCom->Draw();
		
/*
		// could output the plots to file here if you want
		TFile f("labppo_plots.root","RECREATE");
		f.Append(hlabppo_prim);
		f.Append(hlabppo_reem);
		f.Append(glabppo_mfp);
		f.Append(glabppo_opscat);
		f.Append(glabppo_remprob);
		f.Write();
*/
	}	
		if(option == "ndlabppo_noscatt"){
		// labppo_scintillator refractive index
		double RI_labppo[3] = {1.505, 0.0, 0.0 };
		RefIndex(RI_labppo);
		// LABPPO primary emission
		ScintEmissionSpec("text_files/LABPPO_primary_emission.txt");
		// LABPPO remission
		ScintReemissionSpec("text_files/PPO_reemission.txt");
		// LABPPO absorption and scattering
		char *filenames_labppo[3];
		filenames_labppo[0] = "text_files/LAB_absorption.txt";
		filenames_labppo[1] = "text_files/PPO_absorption.txt";
		filenames_labppo[2] = "text_files/Nd_absorption.txt"; 
		double relCont_labppo[3] = {0.99829, 0.001710,0.0001}; 
		double remprob_labppo[3] = {0.0001,0.8,0.0};
		double RSf_labppo = 0.000001;
		double RImean_labppo = 1.505;
		double isocomp_labppo = 4.92e-10;
		AbsScatRemScint(3, relCont_labppo, RSf_labppo, RImean_labppo, isocomp_labppo,
		                filenames_labppo, remprob_labppo);

		// Now make a comparison plot (and rename histograms)
		TH1F *hlabppo_prim = (TH1F*)hscintOut->Clone("hlabppo_prim");
		hlabppo_prim->Scale(50);
		hlabppo_prim->SetAxisRange(0.,1.1,"Y");
		hlabppo_prim->SetYTitle("");
		hlabppo_prim->SetTitle("");
		TH1F *hlabppo_reem = (TH1F*)hremOut->Clone("hlabppo_reem");
		hlabppo_reem->Scale(50);
		hlabppo_reem->SetLineColor(2);
		TGraph *glabppo_mfp = (TGraph*)gROOT->FindObject("gTotmfp");
		glabppo_mfp->SetName("glabppo_mfp");
		TGraph *glabppo_opscat  = (TGraph*)gROOT->FindObject("gfracray");
		glabppo_opscat->SetName("glabppo_opscat");
		TGraph *glabppo_remprob = (TGraph*)gROOT->FindObject("gremprob");
		glabppo_remprob->SetName("glabppo_remprob");
		TCanvas *CanCom = new TCanvas("CanCom");
		CanCom->cd();
		hlabppo_prim->Draw();
		hlabppo_reem->Draw("same");
		glabppo_mfp->Draw("PL");
		glabppo_opscat->Draw("PL");
		glabppo_remprob->Draw("PL");
		TLegend *legCom = new TLegend(0.55,0.28,0.89,0.53);
		legCom->SetBorderSize(0);
		legCom->SetFillColor(0);
		legCom->AddEntry(hlabppo_prim,"Primary Emission Spectrum", "L");
		legCom->AddEntry(hlabppo_reem,"Reemission Spectrum", "L");
		legCom->AddEntry(glabppo_mfp,"Total MFP for extinction in mm", "PL");
		legCom->AddEntry(glabppo_opscat,"Fraction of Attenuation due to Rayleigh", "PL");
		legCom->AddEntry(glabppo_remprob,"Probability of Reemission if absorbed","PL");
		legCom->Draw();
		
/*
		// could output the plots to file here if you want
		TFile f("labppo_plots.root","RECREATE");
		f.Append(hlabppo_prim);
		f.Append(hlabppo_reem);
		f.Append(glabppo_mfp);
		f.Append(glabppo_opscat);
		f.Append(glabppo_remprob);
		f.Write();
*/
	}	if(option == "ndlabppo_noabs"){
		// labppo_scintillator refractive index
		double RI_labppo[3] = {1.505, 0.0, 0.0 };
		RefIndex(RI_labppo);
		// LABPPO primary emission
		ScintEmissionSpec("text_files/LABPPO_primary_emission.txt");
		// LABPPO remission
		ScintReemissionSpec("text_files/PPO_reemission.txt");
		// LABPPO absorption and scattering
		char *filenames_labppo[2];
		filenames_labppo[0] = "text_files/no_absorption.txt";
		filenames_labppo[1] = "text_files/no_absorption.txt";	
		filenames_labppo[2] = "text_files/no_absorption.txt";
		double relCont_labppo[3] = {0.99829, 0.001710,0.0}; 
		double remprob_labppo[3] = {0.0001,0.8,0.0};
		double RSf_labppo = 12.14;
		double RImean_labppo = 1.505;
		double isocomp_labppo = 4.92e-10;
		AbsScatRemScint(3, relCont_labppo, RSf_labppo, RImean_labppo, isocomp_labppo,
		                filenames_labppo, remprob_labppo);

		// Now make a comparison plot (and rename histograms)
		TH1F *hlabppo_prim = (TH1F*)hscintOut->Clone("hlabppo_prim");
		hlabppo_prim->Scale(50);
		hlabppo_prim->SetAxisRange(0.,1.1,"Y");
		hlabppo_prim->SetYTitle("");
		hlabppo_prim->SetTitle("");
		TH1F *hlabppo_reem = (TH1F*)hremOut->Clone("hlabppo_reem");
		hlabppo_reem->Scale(50);
		hlabppo_reem->SetLineColor(2);
		TGraph *glabppo_mfp = (TGraph*)gROOT->FindObject("gTotmfp");
		glabppo_mfp->SetName("glabppo_mfp");
		TGraph *glabppo_opscat  = (TGraph*)gROOT->FindObject("gfracray");
		glabppo_opscat->SetName("glabppo_opscat");
		TGraph *glabppo_remprob = (TGraph*)gROOT->FindObject("gremprob");
		glabppo_remprob->SetName("glabppo_remprob");
		TCanvas *CanCom = new TCanvas("CanCom");
		CanCom->cd();
		hlabppo_prim->Draw();
		hlabppo_reem->Draw("same");
		glabppo_mfp->Draw("PL");
		glabppo_opscat->Draw("PL");
		glabppo_remprob->Draw("PL");
		TLegend *legCom = new TLegend(0.55,0.28,0.89,0.53);
		legCom->SetBorderSize(0);
		legCom->SetFillColor(0);
		legCom->AddEntry(hlabppo_prim,"Primary Emission Spectrum", "L");
		legCom->AddEntry(hlabppo_reem,"Reemission Spectrum", "L");
		legCom->AddEntry(glabppo_mfp,"Total MFP for extinction in mm", "PL");
		legCom->AddEntry(glabppo_opscat,"Fraction of Attenuation due to Rayleigh", "PL");
		legCom->AddEntry(glabppo_remprob,"Probability of Reemission if absorbed","PL");
		legCom->Draw();
		
/*
		// could output the plots to file here if you want
		TFile f("labppo_plots.root","RECREATE");
		f.Append(hlabppo_prim);
		f.Append(hlabppo_reem);
		f.Append(glabppo_mfp);
		f.Append(glabppo_opscat);
		f.Append(glabppo_remprob);
		f.Write();
*/
	}	
}
