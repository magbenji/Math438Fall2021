setwd("Chapter2/")

### Get the data ----
### Read in the raw data to be fit
data <- read.csv("Observations.csv", header = T)

#### Plot the data --------- 
### Let's explore the data visually
plot(data, type="l")

### Data seem to be exponential of some kind
### Try plotting log y
plot(data,type="l", log="y")

### Log y didn't fix it. Try log x instead.
plot(data,type="l", log="x")

### Log x and log y didn't work. Try log-log instead.
plot(data,type="l", log="xy")

### What model does this suggest in the untransformed variables x,y?

#### Creating a basic model -----
### That produced a nice line!
### Let's transform the data
tdata <- log(data)

### Fit the model
summary(m <- lm(Observation ~ Input, tdata))

### Write down the model for the untransformed variables!
exp(coef(m)[1])

#### A slightly different model ----
### We can also fit this using a altered "link" function in glm, try it!
summary(m2 <- glm(Observation ~ log(Input), data, family = gaussian(link = "log")))

#Compare the predictions of the 2 models
plot(predict(m2), predict(m))
abline(a=0,b=1) #add a 1-to-1 line for convenience

#### Comparing models ----
### Let's choose between the models and compare coefficients
### AIC is inappropriate because the y variables are not the same
AIC(m, m2)
### this would say that the first model on the transformed data is better (lower AIC)

# Let's look at the RSS at the original (untransformed) scale
sum((exp(predict(m)) - data$Observation)^2)
sum((predict(m2, type="response") -  data$Observation)^2)
# Using this more appropriate measure, we see that the second model is actually better

coef(m)
coef(m2)

##### MODEL 2 ------

### Simulate data ----
### Generate some random data for which we know the relationship
set.seed(julian(Sys.Date()))
x <- runif(100,0,10)
y <- 4 + (x-2)^2 + runif(100,-1,1)*0.5*x

### Visualized the data
plot(y~x)
xy.lo <- data.frame(x = seq(min(x),max(x),len = 100), y = predict(loess(y~x),data.frame(x=seq(min(x),max(x),len = 100))))
lines(xy.lo)

### See roughly where the loess thinks the bottom of the 
### parabola.
round(min(xy.lo$y))
round(x[which.min(y)])

#### Modeling the data ----
### let's transform the variables
yp <- y - 4
xp <- x - 2

### now plot the variables
### why is using abs() justified?
plot(abs(yp)~abs(xp),log="xy")

### let's try our linear model
m3 <- lm(log(abs(yp))~log(abs(xp)))

### That model had an intercept, which we don't want.
### Run the model again without an intercept.
m4 <- lm(log(abs(yp))~log(abs(xp))-1)

### Now check out the diagnostics
plot(m4) 

### The diagnostics don't look great.
### Let's look at the fit
plot(abs(yp)~abs(xp),log="xy")
abline(m4, col = "red")


### Clearly our fits are missing at the high end of the 
### spectrum due to the low end of the spectrum.
m5 <- lm(log(abs(yp))~log(abs(xp))-1, subset = abs(xp) > 2)

### Add m5's fit to the plot
abline(m5, col = "blue", lty = 2)

### Now look at the diagnostics
plot(m5)

### Much better!!!

### Alternative strategies to fitting the model
### without as much guess work/transformation
summary(m6 <- lm(y ~ x + I(x^2)))
summary(m7 <- lm(y ~ x + offset(x^2)))

### How would we compare which model is best between
### m5, m6, and m7? (Note AIC won't work because the
### data used in the models is different.)

