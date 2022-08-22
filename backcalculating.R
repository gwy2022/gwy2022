
##plot histgramme all in one 
data$date <- as.Date(data$date,'%Y-%m-%d')
data$land <-as.character(data$land)
temp<-read.csv('/Users/wenyaogan/data_new.csv')
temp<-out_data
n<-length(temp$X)
line <- par(lwd = 2) # this changes the thickness of the line in the histogram
hist(temp$fapar_wd, main = "", prob = FALSE, xlim = c(0,1), ylim = c(0,11000),
     border = "black", angle = 45, density = 10, breaks = 8,lwd = 2, xlab = expression('fapar'),
     col = "darkgray", cex.lab = 1.5, cex.axis = 1.75, labels=TRUE)
line <- par(lwd = 3) # I did this because I wanted to coordinate the breaks of the plots to match exactly the same, otherwise the function will choose their own breaks
hist(temp$fapar_sm , main = "", prob = FALSE, add = TRUE,
     xlim = c(0,1), ylim = c(0,1500), breaks = 8,
     border = "darkblue",angle = 135, density = 10,lty = 1, lwd = 2, col = "darkgray")
line <- par(lwd = 3) # I did this because I wanted to coordinate the breaks of the plots to match exactly the same, otherwise the function will choose their own breaks
hist(temp$fapar, main = "", prob = FALSE, add = TRUE,
     xlim = c(0,1), ylim = c(0,11000), breaks = 10,
     border = "darkred", lty = 1, lwd = 2, col = NULL)
hist_legend <- c('fAPARfit_wd','fAPARfit_pmodel','fAPAR_modis')
legend("topright", legend = hist_legend, cex = 1, fill = c("darkgray", "darkgray","white"),
       border = c("black", "darkblue","darkred"), angle = c(45, 135), density = c(25, 25))
title(paste0('n = ',n))


##plot histgramme all by land
for (i in unique(data$land)){
  m = unique(data$land)[8]
  m = 'SAV'
  temp<-out_data[which(out_data$land==m),]
  n<-length(temp$X)
  line <- par(lwd = 2) # this changes the thickness of the line in the histogram
  hist(temp$fapar_wd , main = paste0(m,' (n = ',n,')'), prob = FALSE, xlim = c(0,1), ylim = c(0,1500),
       border = "black", angle = 45, density = 15, breaks = 8,lwd = 2, xlab = expression('fapar'),
       col = "darkgray", cex.lab = 1.5, cex.axis = 1.75, labels=TRUE)
  line <- par(lwd = 3) # I did this because I wanted to coordinate the breaks of the plots to match exactly the same, otherwise the function will choose their own breaks
  hist(temp$fapar_sm , main = "", prob = FALSE, add = TRUE,
       xlim = c(0,1), ylim = c(0,1500), breaks = 8,
       border = "darkblue",angle = 135, density = 10,lty = 1, lwd = 2, col = "darkgray")
  line <- par(lwd = 3) # I did this because I wanted to coordinate the breaks of the plots to match exactly the same, otherwise the function will choose their own breaks
  hist(temp$fapar , main = "", prob = FALSE, add = TRUE,
       xlim = c(0,1), ylim = c(0,1500), breaks = 8,
       border = "darkred", lty = 1, lwd = 2, col = NULL)
  hist_legend <- c('fAPARfit_WD','fAPARfit_pmodel','fAPAR_MODIS')
  legend("topright", legend = hist_legend, cex = 1, fill = c("darkgray", "darkgray","white"),
         border = c("black", "darkblue","darkred"), angle = c(45, 135), density = c(25, 25))

  }


m = unique(data$land)[8]
temp<-data[which(data$land==m)]
temp=data_test
line <- par(lwd = 2) # this changes the thickness of the line in the histogram
hist(temp$wd_8day,main = "Soil mositure factor", prob = FALSE, xlim = c(0,1), ylim = c(0,7000),
     border = "black", angle = 45, density = 15, breaks = 10,lwd = 2, xlab = expression('soil mositure'),
     col = "darkgray", cex.lab = 1.5, cex.axis = 1.75, labels=TRUE)
line <- par(lwd = 3) # I did this because I wanted to coordinate the breaks of the plots to match exactly the same, otherwise the function will choose their own breaks
hist(temp$soilflx, main = "", prob = FALSE, add = TRUE,
     xlim = c(0,1), ylim = c(0,7000), breaks = 10,
     border = "darkblue",lty = 1, lwd = 2, col = NULL)
hist_legend <- c('soil_wd','soil_pmodel')
legend("top", legend = hist_legend, cex = 1, fill = c("darkgray", "white"),
       border = c("black", "darkblue"), angle = c(45, NULL), density = c(25, NULL))

line <- par(lwd = 3) # I did this because I wanted to coordinate the breaks of the plots to match exactly the same, otherwise the function will choose their own breaks
hist(temp$fapar, main = "", prob = FALSE, add = TRUE,
     xlim = c(0,1), ylim = c(0,500), breaks = 8,
     border = "darkred", lty = 1, lwd = 2, col = NULL)


