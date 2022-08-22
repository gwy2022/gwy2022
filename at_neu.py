#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 22:04:40 2022

@author: wenyaogan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 21:34:29 2022

@author: wenyaogan
"""


from matplotlib import pyplot 
import matplotlib.dates as mdates
import numpy as np
from pyrealm import pmodel
import pandas as pd

ds = pd.read_csv('//Users/wenyaogan/Downloads/pmodelproject/workspace/Archive_result/US_Ne3.csv')   ##able to filter different vegetation type
ds['elevation'] = 363
# Extract the six variables for all months
temp = np.array(ds['TA_F'][:])
co2 = np.array(ds['co2_annual'][:] )        # Note - spatially constant but mapped.
elev = np.array(ds['elevation'][:] ) # Note - temporally constant but repeated
vpd = np.array(ds['VPD_F'][:])
fapar = np.array(ds['value'][:])
fapar_pre = np.array(ds['pre_par'])
ppfd = 0.1763* np.array(ds['SW_IN_F'][:]) # PPFD=60×60×24×10−6kECRSW, where kEC=2.04 µmol J−1  #note-splash 
gpp_site =np.array(ds['GPP_NT_VUT_REF'][:]) ## filter
time = np.array(ds['date'][:])
soilm = np.array(ds['sm_lim'][:])
alpha1 = np.array(ds['alpha1'][:])
p_0 = 0.262
p_1 = 0.567
soilmstress_theta0 = p_0 +p_1*alpha1

##
temp[temp < -25] = np.nan
gpp_site[gpp_site <-7000] = np.nan

# Convert elevation to atmospheric pressure
patm = pmodel.calc_patm(elev)


# Clip VPD to force negative VPD to be zero
vpd = np.clip(vpd, 0, np.inf)

# Calculate the photosynthetic environment
env = pmodel.PModelEnvironment(tc=temp,co2=co2, patm=patm, vpd=vpd)
model = pmodel.PModel(env)

soilmstress = pmodel.calc_soilmstress(soilm=soilm,meanalpha=0.8, pmodel_params=pmodel.PModelParams(soilmstress_theta0=0.0, soilmstress_thetastar=0.6, soilmstress_a=0.33490, soilmstress_b=1.456))
model_soil = pmodel.PModel(env,soilmstress = soilmstress, kphio=0.094)

##gpp estimates
ORG = model.estimate_productivity(fapar=fapar, ppfd=ppfd)
ORG = model.gpp
ORG_Mea = model.estimate_productivity(fapar=fapar_pre, ppfd=ppfd)
ORG_Mea =model.gpp
Full_Splash = model_soil.estimate_productivity(fapar=fapar, ppfd=ppfd)
Full_Splash = model_soil.gpp
Full_MeaSp =  model_soil.estimate_productivity(fapar=fapar_pre, ppfd=ppfd)
Full_MeaSp = model_soil.gpp
df = pd.DataFrame(time)
df['time'] = pd.to_datetime(time)
name = 'US_Ne3'
df['ORG'] = ORG
df['ORG_Mea'] =ORG_Mea 
df['ob_gpp'] = gpp_site
df['Full_Splash'] = Full_Splash
df['Full_MeaSp'] = Full_MeaSp
df['site'] = name

df.to_csv ('US_Ne3_full.csv',index = False,sep=',')


##compare gpp difference 
df = df.dropna(axis = 0)
fig1 = pyplot.figure(figsize=(30, 10))
ax = fig1.add_subplot(1, 1, 1)

pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
pyplot.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12)) 
pyplot.plot(df['time'],df['ob_gpp'])
pyplot.plot(df['time'],df['ORG'])
pyplot.plot(df['time'],df['ORG_Mea'])
pyplot.plot(df['time'],df['Full_Splash'])
pyplot.plot(df['time'],df['Full_Splash'])
pyplot.ylim(-1, 20)
pyplot.xlabel('Year')
pyplot.ylabel('GPP g C/m2 8d)')
pyplot.title(name)
pyplot.legend(['Fluxnet','ORG','ORG_Mea','Full_Splash','Full_Splash'],loc='upper right',bbox_to_anchor=(1.1,1),borderaxespad=0)
fig1.tight_layout()
pyplot.savefig('AT_Neu_gpp.png')
pyplot.show()

##compare fapar difference 
fig2 = pyplot.figure(figsize=(20, 5))
ax = fig2.add_subplot(1, 1, 1)

pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
pyplot.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12)) 
pyplot.plot(df['time'],fapar)
pyplot.plot(df['time'],fapar_pre)
pyplot.ylim(0, 1)
pyplot.xlabel('Year')
pyplot.ylabel('FAPAR')
pyplot.title(name)
pyplot.legend(['modis_par','pre_par'],loc='upper right',bbox_to_anchor=(1.1,1),borderaxespad=0)
fig1.tight_layout()
pyplot.savefig('AT_Neu_fapar.png')
pyplot.show()

