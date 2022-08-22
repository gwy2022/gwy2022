##model evaluation
library('datatable')
library('metrics')
library('DescTools')
library('terra')
path<-'/Users/wenyaogan/Downloads/pmodelproject/workspace/fullresultoutput'
fileNames <- dir(path)
filePath <- sapply(fileNames, function(x){
  paste(path,x,sep='/')
})

full_data<- lapply(filePath, function(x){
  read.table(x,header = T,sep = ',')
})

data_plot<-rbindlist(full_data)
classid_vec <- unique(data_plot$site)
data_plot <- na.omit(data_plot)

# Getting the coefficients for each site 
for (i in site) {
  y <- data_plot[data_plot$site == i,]$ob_gpp
  x <- data_plot[data_plot$site == i,]$pre_gpp_sm_site
  print(i)
  rho_coef <- round(CCC(y, x, ci = "z-transform", conf.level = 0.95, na.rm = FALSE)$rho.c$est,2)
  r_squared <- round(summary(lm(y~x))$r.squared,2)
  rmse_coef <- round(rmse(y, x),2)
  pbias_coef <- round(percent_bias(y, x),2)
  exp_1[[i]] = list(paste("~rho[c] ==", rho_coef),
                    paste("~R² ==", r_squared),
                    paste("RMSE ==", rmse_coef),
                    paste("PBIAS ==", pbias_coef))
}

}
### overall evluation
y <- data_plot$ob_gpp
x <- data_plot$pre_gpp_sm_site
rho_coef <- round(CCC(y, x, ci = "z-transform", conf.level = 0.95, na.rm = FALSE)$rho.c$est,2)
r_squared <- round(summary(lm(y~x))$r.squared,2)
rmse_coef <- round(rmse(y, x),2)
pbias_coef <- round(percent_bias(y, x),2)
exp_1[[i]] = list(paste("~rho[c] ==", rho_coef),
                    paste("~R² ==", r_squared),
                    paste("RMSE ==", rmse_coef),
                    paste("PBIAS ==", pbias_coef))
