

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import netCDF4
import numpy as np
from pyrealm import pmodel
import pandas as pd
import xarray as xr
from matplotlib import pyplot



##read fapar
dataset =xr.open_rasterio(r'/Users/wenyaogan/Downloads/modis 8day/2013 modis.tif')

im_data = dataset[1:47,:,:]
##qair
Qair_wfde = xr.open_dataset('/Users/wenyaogan/downloads/Qair_8day/Qair_daytime_WFDE5_CRU_2013_v1.0_8day.nc')
Qair = Qair_wfde.variables['Qair']
sw_wfde = xr.open_dataset('/Users/wenyaogan/downloads/SW_down_8day/SWdown_WFDE5_CRU_2013_v1.0_8day.nc')
sw = sw_wfde.variables['SWdown']
tair_wfde=xr.open_dataset('/Users/wenyaogan/downloads/Tair_8day/Tair_daytime_WFDE5_CRU_2013_v1.0_8day.nc')
tair = tair_wfde.variables['Tair']
##co2
co2 =pd.read_csv('/Users/wenyaogan/monthly_in_situ_co2_mlo.csv') 
co2 = co2[288+12*7:288+12*8] ##2006
co2 = np.mean(co2['6'])
##elevation
elev = xr.open_dataset("/Users/wenyaogan/Desktop/WFDEI-elevation.nc")
self_elev = elev.variables['elevation']
wd= xr.open_dataset('/Users/wenyaogan/wd_stress.nc')
wd= wd.variables['variable'][:]
year = 2013
num = (year-2003) * 46
number = num+46
wd2 = wd[num:number,:,:]

##R
Rd = 8.314/28.963
Rv  =8.314/18.02
        
## pmodel run

gpp_2013= np.zeros(shape=(46, 360, 720))
gpp_2013_modis = np.zeros(shape=(46, 360, 720))
for num in range(0, 46):
    ###temperature
    self_tmp = np.asarray(tair[num,:, :])
    tair_degree = self_tmp-273.15
    tair_degree[tair_degree <= -25] = float('nan')

    ###ppfd
    self_ppfd = np.asarray(sw[num,:, :] * 2.04/1000)*8 # convert radiation to ppfd

    selfp = np.asarray(self_elev)
    
    self_co2 = co2
    
    self_p = pmodel.calc_patm(selfp)
    ##fapar
    fapar = im_data[num,:,:]
    fapar = np.flipud(fapar)
    self_fapar =np.asarray(fapar)
    self_fapar[self_fapar < 0] = float('nan')
    ##calculating vpd
    ###vpd
    esat = 611*2.71828**((tair_degree*17.27)/(tair_degree+237.3))
    q_air = np.asarray(Qair[num,:,:])
    wair = q_air/(1-q_air)
    eact = (self_p*wair*Rv)/(Rd+wair*Rv)
    self_vpd = esat-eact
    self_vpd[self_vpd < 0] = 0
    ##    
    selfwd = np.asarray(wd2)
    selfwd = np.flipud(selfwd[num,:,:])
    env = pmodel.PModelEnvironment(tc=tair_degree,vpd=self_vpd, co2=self_co2, patm=self_p) # calculating environment


    # Estimate GPP
    model= pmodel.PModel(env,soilmstress = selfwd)
    model.estimate_productivity(fapar=self_fapar,ppfd=self_ppfd)
    model1= pmodel.PModel(env)
    model1.estimate_productivity(fapar=self_fapar,ppfd=self_ppfd)
    gpp_2013[num,:, :] = model.gpp
    gpp_2013_modis[num,:, :] = model1.gpp


