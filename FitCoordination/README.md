# Fit Coordination
The sub-folders located here contain the coordinators used to (re)generate the .ratdb parameters used by the various fitter components and classifiers in RAT.    
Please consult the individual READMEs for each coordinator for instructions on how to run them.  

-------------------------

## WaterFitter

The waterFitter contains the following components that require coordinating and require no pre-requisites:  

- seed method for position reconstruction: "quad" - coordinate using **"QuadSpeed"**
- PDF for position reconstruction: "gv1d" - coordinate using **"HitTimePDF"**
- main method for nearAV position reconstruction: "nearAVAngular" - coordinate using **"NearAVAngular"**
- energy method: "energyLookup" - coordinate using **"EnergyLookup"**
- PDF for direction reconstruction: "positionDirectionPDF" - coordinate using **"DirectionPDF"**
- **ScintEffectiveSpeed** (see below)

The following components of the waterFitter use the effective speed of light in scintillator as part of their coordination, and so should be coordinated only **after "ScintEffectiveSpeed"**:  

- ITR classifier - coordinate using **[no coordinator as of writing]**
- QPDT classifier - coordinate using **[no coordinator as of writing]**

-------------------------

## ScintFitter

The scintFitter contains the following components that require coordinating and require no pre-requisites:  

- seed method for position reconstruction: "quad" - coordinate using **"QuadSpeed"**
- PDF for position reconstruction: "et1d" - coordinate using **"HitTimePDF"**
- main method for nearAV position reconstruction: "nearAVAngular" - coordinate using **"NearAVAngular"**
- **ScintEffectiveSpeed** (see below)

The following components of the scintFitter use the effective speed of light in scintillator as part of their coordination, and so should be coordinated only **after** "ScintEffectiveSpeed":  

- ITR classifier - coordinate using **[no coordinator as of writing]**
- QPDT classifier - coordinate using **[no coordinator as of writing]**

The following components of the scintFitter use the effective speed of light in scintillator as well as reconstructed position and time as part of their coordination, and so should be coordinated only **after** "ScintEffectiveSpeed", "QuadSpeed" and "HitTimePDF":  

- energy method: "energyFunctional" - coordinate using **"EnergyFunctional"**
- BiPo classifier (Log-Likelihood Difference method, both 212 and 214) - coordinate using **BiPoLikelihoodDiff**
- AlphaBeta classifier (both 212 and 214) - coordinate using **AlphaBetaLikelihood**

The following components of the scintFitter use the effective speed of light in scintillator as well as reconstructed position, time and energy as part of their coordination, and so should be coordinated only **after** "ScintEffectiveSpeed", "QuadSpeed", "HitTimePDF" and "EnergyFunctional":  

- BiPo classifier (Cumulative Time Residuals method) - coordinate using **BiPoCumulTimeResid**

-------------------------

## Other Coordinators

The following coordinators partner fitter/classifier components that are not part of either the waterFitter or scintFitter:  

- **SimpleEnergy**
- **AlphaUnseeded**
- **AlphaSeeded** - this requires the effective speed of light in scintillator as well as reconstructed position and time, and so should be coordinated only **after** "ScintEffectiveSpeed", "QuadSpeed" and "HitTimePDF"

The following coordinators are now redundant, but have been kept as alternate methods:  

- **EffectiveTransit** - superceded by "ScintEffectiveSpeed"
- **EmissionTimePDF** - superceded by "HitTimePDF"

