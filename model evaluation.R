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

# Getting the coefficients
for (i in classid_vec) {
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

for (i in classid_vec) {
  max_scale <- max(data_plot[data_plot$classid == i,]$ob_gpp,data_plot[data_plot$classid == i,]$gpp_full,data_plot[data_plot$classid == i,]$pre_gpp_sm_site)
  n_count <- length(data_plot[data_plot$classid == i,]$ob_gpp)
  assign(i,
         ggplot(data = data_plot[data_plot$classid == i,]) +
           geom_pointdensity(aes(x = pre_gpp_sm_site, y = ob_gpp)) +
           scale_color_viridis(name = "Neighbor point \ndensity") +
           theme_heatmap +
           theme(legend.position = c(.2,.75), legend.title = element_text(size = 10),
                 legend.text = element_text(colour="black", size = 10, face="bold")) +
           ylim(0,max_scale) + xlim(0,max_scale) +
           geom_abline(slope = 1, intercept = 0, lwd = 1) +
           geom_smooth(aes(x = pre_gpp_sm_site, y = ob_gpp), method = "lm", color = "red") +
           xlab("") + ylab("") +
           #xlab(expression(paste("P-model Default GPP (g C m"^"-2", " d"^"-1",")"))) +
           #ylab(expression(paste("FLUXNET2015 GPP (g C m"^"-2", " d"^"-1",")"))) +
           annotate(geom = "text", #x = 12.5, y = 2.5, size = 5,
                    x = 0.8*max_scale, y = seq(0.17*max_scale, 0.01, length = 4), size = 5,
                    label = exp_1[[i]], parse = TRUE) +
           annotate(geom = "text", x = 0.97*max_scale, y = max_scale, size = 4,
                    label = "1:1", angle = 45) +
           annotate(geom = "text", x = 0.075*max_scale, y = 0.505*max_scale, size = 3,
                    label = paste("n =", n_count))
  )
}

