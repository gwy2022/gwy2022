#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 23:57:38 2022

@author: wenyaogan
"""


from matplotlib import pyplot 
import matplotlib.dates as mdates
import numpy as np
from pyrealm import pmodel
import pandas as pd

ds = pd.read_csv('/Users/wenyaogan/Downloads/pmodelproject/workspace/Archive_result/DE_Tha.csv')   ##able to filter different vegetation type
ds['elevation'] = 380
# Extract the six variables for all months
temp = np.array(ds['TA_F'][:])
co2 = np.array(ds['CO2'][:] )        # Note - spatially constant but mapped.
elev = np.array(ds['elevation'][:] ) # Note - temporally constant but repeated
vpd = np.array(ds['VPD_F'][:])
fapar = np.array(ds['value'][:])
ppfd = 0.1763* np.array(ds['SW_IN_F'][:]) # PPFD=60×60×24×10−6kECRSW, where kEC=2.04 µmol J−1  #note-splash 
gpp_site = 8*np.array(ds['GPP_NT_VUT_REF'][:]) ## filter
time = np.array(ds['date'][:])
alpha = np.array(ds['alpha'][:])
alpha1 = np.array(ds['alpha1'][:])
soilm = np.array(ds['sm_lim'][:])
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


df1 = pd.DataFrame(time)
df1['time'] = pd.to_datetime(time)
df1['soilm'] = np.array(ds['sm_lim'][:])
fig3 = pyplot.figure(figsize=(20, 5))
ax = fig3.add_subplot(1, 1, 1)

pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
pyplot.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12)) 
pyplot.plot(df1['time'],df1['soilm'])
pyplot.xlabel('Year')
pyplot.ylabel('soil moitsure')
pyplot.title('DE_Tha')
pyplot.legend(['soil moitsure'],loc='upper right',bbox_to_anchor=(1.1,1),borderaxespad=0)
fig3.tight_layout()
pyplot.savefig('DE_Tha_sm.png')
pyplot.show()

# Calculate the photosynthetic environment
env = pmodel.PModelEnvironment(tc=temp,co2=co2, patm=patm, vpd=vpd)
model = pmodel.PModel(env)
env.summarize()
##modis par gpp 
modis_gpp = model.estimate_productivity(fapar=fapar, ppfd=ppfd)
modis_gpp =model.gpp
##set sm default
soilmstress = pmodel.calc_soilmstress(soilm=0.6,meanalpha=1 ,pmodel_params=pmodel.PModelParams(soilmstress_theta0=0.0, soilmstress_thetastar=0.6, soilmstress_a=0.0, soilmstress_b=0.685))
model_soil = pmodel.PModel(env,soilmstress = soilmstress)
##modis gpp sm
model_soil.estimate_productivity(fapar=fapar, ppfd=ppfd)
modis_gpp_sm =model_soil.gpp
##environment sm soil moiture function
soilmstress_site= pmodel.calc_soilmstress(soilm=soilm,meanalpha=alpha1 ,pmodel_params=pmodel.PModelParams(soilmstress_theta0=np.mean(soilmstress_theta0), soilmstress_thetastar=0.9))
#As for methods βa and βc, θ0 = 0.0 and θ∗ = 0.9.
model_soil1 = pmodel.PModel(env,soilmstress = soilmstress_site)
##modis gpp sm_site
model_soil1.estimate_productivity(fapar=fapar, ppfd=ppfd)
modis_gpp_sm_site =model_soil1.gpp


                    
                              

df = pd.DataFrame(time)
df['time'] = pd.to_datetime(time)
name = 'DE_Tha'
df['modis_gpp'] = modis_gpp 
df['ob_gpp'] = gpp_site
df['modis_gpp_sm'] =modis_gpp_sm
df['modis_gpp_site'] = modis_gpp_sm_site 
df['site'] = name



df.to_csv ('DE_Tha_full.csv',index = False,sep=',')
##compare gpp difference 

fig1 = pyplot.figure(figsize=(20, 5))
ax = fig1.add_subplot(1, 1, 1)

pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
pyplot.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12)) 
pyplot.plot(df['time'],df['ob_gpp'])
pyplot.plot(df['time'],df['modis_gpp'])
pyplot.plot(df['time'],df['modis_gpp_sm'])
pyplot.plot(df['time'],df['modis_gpp_site'])
pyplot.ylim(-1, 20)
pyplot.xlabel('Year')
pyplot.ylabel('GPP g C/m2 8d)')
pyplot.title(name)
pyplot.legend(['ob_gpp','modis_gpp','modis_gpp_sm','modis_gpp_sm_site'],loc='upper right',bbox_to_anchor=(1.11,1),borderaxespad=0)
fig1.tight_layout()
pyplot.savefig('DE_Tha_gpp.png')
pyplot.show()