# Fit Plots Tools
These tools are a quick and simple way of plotting the fit results.

## Usage
These tools are for usage in root's cint, thus to use load root and type:

    .X $RATTOOLS/FitPlots/Load.c
    PlotPosition( filename )

### Retriggered Events
To have the plotting tools ignore retriggered events whilst plotting, set (after the load command):

    gIgnoreRetriggeres = true;
   
### Common error
If you get a [Something]_cc.so file not found error, execute:

    .X $RATTOOLS/FitPlots/Delete.c

Reload root and try again.

## Details
Full details are available in DocDB-982, https://www.snolab.ca/snoplus/private/DocDB/cgi/ShowDocument?docid=982.
