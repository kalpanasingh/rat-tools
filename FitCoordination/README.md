# Fit Coordination
The sub-folders located here contain the coordinators used to (re)generate the .ratdb parameters used by the various fitter components and classifiers in RAT.    
Please consult the individual READMEs for each coordinator for instructions on how to run them.  

-------------------------

## WaterFitter

The waterFitter contains the following components that require coordinating and require no pre-requisites:  

- seed method for position reconstruction: "quad" - coordinate using **"QuadSpeed"**
- PDF for position reconstruction: "gv1d" - coordinate using **"HitTimePDF"**
- energy seed: "energyPromptLookup" - coordainte using **"EnergyPromptLookup"**
- energy method: "energyRSP" - coordinate in two stages using **"EnergyRSP-Part1"** and **"EnergyRSP-Part2"**
- PDF for direction reconstruction: "positionDirectionPDF" - coordinate using **"DirectionPDF"**

The following classifiers currently have no coordinators:

- ITR classifier - coordinate using **[no coordinator as of writing]**
- QPDT classifier - coordinate using **[no coordinator as of writing]**

-------------------------

## ScintFitter

The scintFitter contains the following components that require coordinating and require no pre-requisites:  

- seed method for position reconstruction: "quad" - coordinate using **"QuadSpeed"**
- main method for energy reconstruction: "energyRThetaFunctional" - coordinate using **"EnergyRThetaFunctional"**
- method for removal of near AV events: "positionANN" - coordinate using **"PositionANN"**

The following components depend on one another, and so must be coordinated in an iterative manner:

- EffectiveVelocity values - coordainte using **ScintEffectiveSpeed**
- PDF for position reconstruction: "et1d" - coordinate using **"HitTimePDF"**

**ScintEffectiveSpeed** provides an effective velocity value in scintillator by minimising bias from the scintFitter, which in turn requires an effective velocity for the ET1D PDF to calculate hit time residuals.  The only solution to this is to run the two coordinators in turn until the difference in the new "inner_av_velocity" from "ScintEffectiveSpeed" is small compared to the old value (where small is less than 0.5% difference).  Note that this iterative process can be sped up by using batch systems to produce data and following this process for coordination:

- Coordinate **ScintEffectiveSpeed**
  - If running with a new material, run "python -c 'import Utilities.py; Utilities.DrawPlot()'" once complete to check that the range of effective velocities tested are appropriate;
- Update appropriate EFFECTIVE_VELOCITY RATDB values;
- Coordinate **HitTimePDF**;
- Update appropriate ET1D RATDB values;
- The following stages may now be iterated"
  - Coordinate **ScintEffectiveSpeed** as above;
  - Rerun the **HitTimePDF** analysis function (HitTimePDF/AnalyseData.py) with the -v option to override the effective velocity.

The following components of the scintFitter use the effective speed of light in scintillator as part of their coordination, and so should be coordinated only **after** "ScintEffectiveSpeed":  

- ITR classifier - coordinate using **[no coordinator as of writing]**
- QPDT classifier - coordinate using **[no coordinator as of writing]**

The following components of the scintFitter use the effective speed of light in scintillator as well as reconstructed position and time as part of their coordination, and so should be coordinated only **after** "ScintEffectiveSpeed", "QuadSpeed" and "HitTimePDF":  

- BiPo classifier (Log-Likelihood Difference method, both 212 and 214) - coordinate using **BiPoLikelihoodDiff**
- AlphaBeta classifier (both 212 and 214) - coordinate using **AlphaBetaLikelihood**
- BerkeleyAlphaBeta classifier - coordinate using **BerkeleyAlphaBeta**

The following components of the scintFitter use the effective speed of light in scintillator as well as reconstructed position, time and energy as part of their coordination, and so should be coordinated only **after** "ScintEffectiveSpeed", "QuadSpeed", "HitTimePDF" and "EnergyRThetaFunctional":  

- BiPo classifier (Cumulative Time Residuals method) - coordinate using **BiPoCumulTimeResid**

-------------------------

## PEnergy

PEnergy requires "re-coordination" in two circumstances:
   - When there is a change to the 3-d PMT model
   - When there is a change to the scintillator cocktail that results in a
      change in the numbers of scintillation or Cherenkov photons produced 
      as a function of event energy.

-------------------------

## Other Coordinators

The following coordinators partner fitter/classifier components that are not part of either the waterFitter or scintFitter:  

- **SimpleEnergy**
- **AlphaUnseeded**
- **AlphaSeeded** - this requires the effective speed of light in scintillator as well as reconstructed position and time, and so should be coordinated only **after** "ScintEffectiveSpeed", "QuadSpeed" and "HitTimePDF"
- **EnergyLookup** - replaced by **EnergyRSP** and **EnergyPromptLookup** in the waterFitter
- **EnergyFunctional** - replaced by "EnergyRThetaFunctional" in the scintFitter
- **NearAVAngular** - for the "nearAVAngular" fit method
  - Note, a classifier also called "nearAVAngular" **is** used by the scintFitter

The following coordinators are now redundant, but have been kept as alternate methods:  

- **EffectiveTransit** - superceded by "ScintEffectiveSpeed"
- **EmissionTimePDF** - superceded by "HitTimePDF"

