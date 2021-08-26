setwd("~/Dropbox/Documents/Teaching/Mathematical Modeling")

install.packages("deSolve")
install.packages("ggplot2")
install.packages("optimx")
library(deSolve)
library(ggplot2)
library(optimx)

ctl <- c(4.17,5.58,5.18,6.11,4.50,4.61,5.17,4.53,5.33,5.14)
trt <- c(4.81,4.17,4.41,3.59,5.87,3.83,6.03,4.89,4.32,4.69)
group <- gl(2, 10, 20, labels = c("Ctl","Trt"))
weight <- c(ctl, trt)
lm.D9 <- lm(weight ~ group)


x <- 2
y <- 3L #declare integer

x*y
x+y
x^3
x**3
x-y

x <- c(1,6,2,4)
y <- c(2,1,3)

z <- matrix(y,nrow=2,ncol=3)
z <- matrix(y,nrow=2,ncol=3, byrow=T)

###read data!

digoxin <- read.csv("Digoxin.csv", header = T)

digoxin$Visit <- as.Date(digoxin$Visit, format = "%m/%d/%y")

digoxin$Weight <- as.numeric(as.character(digoxin$Weight))
digoxin$Weight[1] <- 70

as.numeric(digoxin$Visit)

##### BEGIN ANALYSIS
library(ggplot2)

g <- ggplot(data=digoxin, aes(x=Visit, y=mM_Digoxin, group = Subject))

#note plus sign at end of line to add a linebreak in the ggplot command
g + geom_line(aes(color = Subject)) + theme_bw() + ylab("mM digoxin") + xlab("Visit (time)") +
   ggtitle("Digoxin Levels over Time")


lm(mM_Digoxin ~ Weight + I(sin(2*pi/30*Visit)), data=digoxin)

m1 <- lm(mM_Digoxin ~ Weight + I(sin(2*pi/30*as.numeric(Visit))), data=digoxin)
summary(m1)

m2 <- lm(mM_Digoxin ~ Weight + I(sin(2*pi/30*as.numeric(Visit))) - 1, data=digoxin)
summary(m2)

anova(m1,m2) #m2 would be favored
plot(m2)

digoxin$predicted <- predict(m2)

g <- ggplot(data=digoxin, aes(x=Visit, y=mM_Digoxin, group = Subject))

g + geom_line(aes(color = Subject)) + geom_line(aes(y=predicted, color = Subject), lty = 2) + 
  theme_bw() + ylab("mM digoxin") + 
  xlab("Visit (time)") +
  ggtitle("Digoxin Levels over Time with Fits")


### let's try lagging the time variable because we don't know what day = 0

plot(I(sin(as.numeric(digoxin$Visit)*2*pi/30))[1:20], type="l") #high level plot command
lines(I(sin((as.numeric(digoxin$Visit)-15)*2*pi/30))[1:20], type="l", col="red") #low level command


###we'll loop over lags and see which is best

findLag <- data.frame(lag=0:29, aic = NA)

for(i in 1:nrow(findLag)){
  lag <- findLag$lag[i]
  findLag$aic[i] <- with(digoxin,{
    time <- as.numeric(Visit) - lag
    trans_time <- sin(time * 2 * pi / 30)
    model <- lm(mM_Digoxin ~ Weight + trans_time - 1)
    AIC(model)
  })
}

plot(findLag, type = "l")
min(findLag$aic)
bestLag <- findLag$lag[which.min(findLag$aic)]

###now run the model using bestLag

m3 <- lm(mM_Digoxin ~ Weight + I(sin(2*pi/30*(as.numeric(Visit) - bestLag))) - 1, data=digoxin)
summary(m3)

digoxin$lag_predicted <- predict(m3)

g <- ggplot(data=digoxin, aes(x=Visit, y=mM_Digoxin, group = Subject))

g + geom_line(aes(color = Subject)) + geom_line(aes(y=predicted, color = Subject), lty = 2) +
  geom_line(aes(y=lag_predicted, color = Subject), lty = 3) +
  theme_bw() + ylab("mM digoxin") + 
  xlab("Visit (time)") +
  ggtitle("Digoxin Levels over Time with Fits from 2 Models")


