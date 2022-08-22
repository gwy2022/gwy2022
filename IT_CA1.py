#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 20:55:45 2022

@author: wenyaogan
"""

from matplotlib import pyplot 
import matplotlib.dates as mdates
import numpy as np
from pyrealm import pmodel
import pandas as pd

ds = pd.read_csv('/Users/wenyaogan/Downloads/pmodelproject/workspace/Archive_result/IT_CA1.csv')   ##able to filter different vegetation type
ds['elevation'] = 50
# Extract the six variables for all months
temp = np.array(ds['TA_F'][:])
co2 = np.array(ds['CO2'][:] )        # Note - spatially constant but mapped.
elev = np.array(ds['elevation'][:] ) # Note - temporally constant but repeated
vpd = np.array(ds['VPD_F'][:])
fapar = np.array(ds['value'][:])
fapar_pre = np.array(ds['pre_par'])
ppfd = 0.1763* np.array(ds['SW_IN_F'][:]) # PPFD=60×60×24×10−6kECRSW, where kEC=2.04 µmol J−1  #note-splash 
gpp_site = np.array(ds['GPP_NT_VUT_REF'][:]) ## filter
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
pyplot.title('IT_CA1')
pyplot.legend(['soil moitsure'],loc='upper right',bbox_to_anchor=(1.1,1),borderaxespad=0)
fig3.tight_layout()
pyplot.savefig('IT_CA1_sm.png')
pyplot.show()

# Clip VPD to force negative VPD to be zero
vpd = np.clip(vpd, 0, np.inf)

# Calculate the photosynthetic environment
env = pmodel.PModelEnvironment(tc=temp,co2=co2, patm=patm, vpd=vpd)
model = pmodel.PModel(env)
env.summarize()
##pre_par gpp
model.estimate_productivity(fapar=fapar_pre, ppfd=ppfd)
pre_gpp = model.gpp
##modis par gpp 
modis_gpp = model.estimate_productivity(fapar=fapar, ppfd=ppfd)
modis_gpp =model.gpp
##set sm default
soilmstress = pmodel.calc_soilmstress(soilm=0.6,meanalpha=1 ,pmodel_params=pmodel.PModelParams(soilmstress_theta0=0.0, soilmstress_thetastar=0.6, soilmstress_a=0.0, soilmstress_b=0.685))
model_soil = pmodel.PModel(env,soilmstress = soilmstress)
##pre_gpp sm
model_soil.estimate_productivity(fapar=fapar_pre, ppfd=ppfd)
pre_gpp_sm = model_soil.gpp
##modis gpp sm
model_soil.estimate_productivity(fapar=fapar, ppfd=ppfd)
modis_gpp_sm =model_soil.gpp
##environment sm soil moiture function
soilmstress_site= pmodel.calc_soilmstress(soilm=soilm,meanalpha=alpha1 ,pmodel_params=pmodel.PModelParams(soilmstress_theta0=np.mean(soilmstress_theta0), soilmstress_thetastar=0.9))
#As for methods βa and βc, θ0 = 0.0 and θ∗ = 0.9.
model_soil1 = pmodel.PModel(env,soilmstress = soilmstress_site)
##pre_gpp sm_site
model_soil1.estimate_productivity(fapar=fapar_pre, ppfd=ppfd)
pre_gpp_sm_site = model_soil1.gpp
##modis gpp sm_site
model_soil1.estimate_productivity(fapar=fapar, ppfd=ppfd)
modis_gpp_sm_site =model_soil1.gpp



                    
                              

df = pd.DataFrame(time)
df['time'] = pd.to_datetime(time)
name = 'IT_CA1'
df['modis_gpp'] = modis_gpp 
df['pre_gpp'] =pre_gpp 
df['ob_gpp'] = gpp_site
df['pre_gpp_sm'] = pre_gpp_sm 
df['pre_gpp_sm_site'] = pre_gpp_sm_site
df['modis_gpp_sm'] =modis_gpp_sm
df['modis_gpp_sm_site'] = modis_gpp_sm_site 
df['site'] = name
df.to_csv ('IT_CA1_full.csv',index = False,sep=',')


##compare gpp difference 

##compare gpp difference 

fig1 = pyplot.figure(figsize=(30, 10))
ax = fig1.add_subplot(1, 1, 1)

pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
pyplot.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12)) 
pyplot.plot(df['time'],df['ob_gpp'])
pyplot.plot(df['time'],df['modis_gpp'])
pyplot.plot(df['time'],df['pre_gpp'])
pyplot.plot(df['time'],df['modis_gpp_sm'])
pyplot.plot(df['time'],df['pre_gpp_sm'])
pyplot.plot(df['time'],df['pre_gpp_sm_site'])
pyplot.plot(df['time'],df['modis_gpp_sm_site'])
pyplot.ylim(-1, 20)
pyplot.xlabel('Year')
pyplot.ylabel('GPP g C/m2 8d)')
pyplot.title(name)
pyplot.legend(['ob_gpp','modis_gpp','pre_gpp','modis_gpp_sm','pre_gpp_sm','pre_gpp_sm_site','modis_gpp_sm_site'],loc='upper right',bbox_to_anchor=(1.1,1),borderaxespad=0)
fig1.tight_layout()
pyplot.savefig('IT_CA1_gpp.png')
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
pyplot.savefig('IT_CA1_fapar.png')
pyplot.show()