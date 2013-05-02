## Chris Jones written 30/04/2013
## This script is used to generate the Supernova neutrino spectrum at 10KPc
## using equation (3) from Physical Review D 83, 113006 (2011) by Basudeb and John F. Beacom [DOI 10.1103/PhyscRevD.83.113006]

##This produces a file which can go into the RAT Database. 

import math,sys
from Numeric import *

pi = math.acos(-1.0)

def faeq(energy_alpha,nu_energy):
	distance = 1.0 			## in units of 10kpc 
	sn_energy_alpha = 5.0 	##in units of 10^52 ergs 
	main_factor = sn_energy_alpha/(distance*distance)
	main_factor = main_factor*(math.pow(nu_energy,3.0))/(math.pow(energy_alpha,5.0))	
	expon_factor = math.exp(-1.0*4.0*nu_energy/energy_alpha)
	main_factor = 2.35e13*main_factor*expon_factor
	return main_factor

## sums the flux over many energy levels 
def sum_faeq(nu_energy,alpha_list):
	summ = 0.0 
	for j in range(0,len(alpha_list)): 
		summ = summ + faeq(alpha_list[j],nu_energy)
	return summ 

nu_energy_max = 50.0 	

## This section of the script writes the RATDB file 
############################################################

num_steps = 1000
alpha_list = [12.0,15.0,18.0,18.0,18.0,18.0] ##in Mev this is the average thermalised energy of a given neutrino flavour
flux_array = zeros((num_steps,7),Float)
sum_flux_array = zeros(7,Float)
nu_energy_array = zeros(num_steps,Float)
delta_nu_energy = nu_energy_max/float(num_steps)
max_array = zeros(7,Float)

for p in range(0,num_steps):
	nu_energy =  float(p)*delta_nu_energy
	flux_array[p][0] = sum_faeq(nu_energy,alpha_list)
	sum_flux_array[0] = sum_flux_array[0] + flux_array[p][0]*delta_nu_energy

	for q in range(1,7):
		flux_array[p][q] = faeq(alpha_list[q-1],nu_energy)
		sum_flux_array[q] = sum_flux_array[q-1] + flux_array[p][q-1]*delta_nu_energy

	nu_energy_array[p] = nu_energy 
	

#Normalising the various spectra
for k in range(0,num_steps):
	for j in range(0,7):
		flux_array[k][j] = flux_array[k][j]/sum_flux_array[j]


f = open('pes_spectrum.ratdb','w')
neutrinoFlavourList = ['all','nu_e','anti_nu_e','nu_mu','anti_nu_mu','nu_tau','anti_nu_tau']
counter = 0
for member in neutrinoFlavourList:
	print member, counter
	f.write('{\nname:"pes_spectrum",\nindex: "SN_' + member + '",\nvalid_begin: [0, 0], \nvalid_end:[0, 0], \nemin: 0.0, \nemax: ' + str(nu_energy_array[num_steps-1]) +  ', \nprobmin: ' + str(min(flux_array)[counter]) +', \nprobmax: '+ str(max(flux_array)[counter]) +', \nspec_energy:[')

	## write the energy table
	for loop in range(0,num_steps) :
			if (loop >= num_steps -1):
				f.write(str(float(nu_energy_array[loop])) +'],\n')
			else:
				f.write(str(float(nu_energy_array[loop])) + ',')
	f.write('\nspec_flux:[')

	##write the flux table 
	for loop in range(0,num_steps) :
			if (loop >= num_steps -1):
				f.write(str(float(flux_array[loop][counter])) +'],\n')
			else:
				f.write(str(float(flux_array[loop][counter])) + ',')
	f.write('}\n\n')
	counter = counter + 1
f.close()




