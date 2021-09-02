import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.getcwd()
os.chdir("/Users/bridenho/Dropbox/GitHub/Math438Fall2021/Chapter2/")

data = pd.read_csv("Observations.csv")


#### Plot the data --------- 
### Let's explore the data visually
plt.plot('Input', 'Observation', data = data)
plt.xlabel('Input')
plt.ylabel('Observation')
plt.grid()
plt.show()


### Data seem to be exponential of some kind
### Try plotting log y
plt.yscale('log')
plt.show()


### Log y didn't fix it. Try log x instead.
plt.yscale('linear')
plt.xscale('log')
plt.show()

### Log x and log y didn't work. Try log-log instead.
plt.yscale('log')
plt.show()
plt.close()


#### Creating a basic model -----
### That produced a nice line!
### Let's transform the data
tdata = np.log(data)

import statsmodels.api as sm
import statsmodels.formula.api as smf

model = smf.ols('Observation ~ Input', data = tdata)
results = model.fit()
results.summary()

results.params['Input'] #get slope for Input
results.params['Intercept']

#try using a GLM model
m2 = smf.glm('Observation ~ np.log(Input)', data = data, family = sm.families.Gaussian(link=sm.families.links.log))
results2 = m2.fit()
results2.summary()

results2.params['np.log(Input)'] #get slope for Input
results2.params['Intercept']

#Compare the predictions of the 2 models
plt.scatter(np.exp(results.predict()), results2.predict())
plt.xlabel('Model 1: OLS on transformed variables')
plt.ylabel('Model 2: GLM with log-link')
plt.axline((0, 0), (1, 1), linewidth=1, color='r')
plt.show()
plt.close()

#Using AIC (which is inappropriate due to differences in y values)
#Note: The AIC values are slightly different in Python vs. R
results.aic
results2.aic 

#RSS at the original scale is a better comparator
np.sum((np.exp(results.predict()) - data.Observation) ** 2)
np.sum((results2.predict() - data.Observation) ** 2)
#The second model (GLM) is better



##### MODEL 2 ------
### 
### We'll do some random number generation to create a known model
### with error.

seed = int(pd.Timestamp.to_julian_date(pd.to_datetime("today")))
rng = np.random.default_rng(seed)


x = rng.uniform(0,10,100)
y = 4 + (x-2) ** 2 + rng.uniform(-1,1,len(x))*0.5*x #true model is x^2 - 4x + 8

#use a smoother to visualize the local trends
from loess.loess_1d import loess_1d #PyPI (Python Package Index) install with pip, just get the function

x_lo, y_lo, w_lo = loess_1d(x,y,frac=0.75,degree=2, xnew = np.arange(0,10,0.01)) #0.75 is the default R parameter for this, as is degree = 2

plt.scatter(x,y)
plt.plot(x_lo, y_lo, color = 'red')
plt.show()
plt.close()

### See roughly where the loess thinks the bottom of the 
### parabola.
round(min(y_lo)) # 4
round(x_lo[np.where(y_lo == min(y_lo))[0].item()]) # 2

#### Modeling the data ----
### let's transform the variables
yp = y - 4
xp = x - 2

### now plot the variables
### why is using abs() justified?
plt.scatter(np.abs(xp), np.abs(yp))
plt.show()

#doesn't look particularly linear; let's try log scale
plt.xscale('log')
plt.show()
plt.yscale('log')
plt.show()

##Using a log-log plot produces something linear looking!
##Let's model that.
xy_data = pd.DataFrame(data={'xp':xp, 'yp':yp})

model3 = smf.ols('np.log(np.abs(yp)) ~ np.log(np.abs(xp))', data=xy_data)
results3 = model3.fit()
results3.summary()

##unfortunately, our Python library doesn't have diagnostic plots,
##but someone has been nice enough to do this elsewhere
##the next statement requires OLSplot.py to be in the current directory
import OLSplot

OLSplot.allplots(results3)
plt.show()
plt.close()


##Because we think our data are quadratic, and we've transformed them
##in a way that should produce the point (0,0), what if tried dropping
##the intercept in the model?

model4 = smf.ols('np.log(np.abs(yp)) ~ np.log(np.abs(xp)) - 1', data=xy_data)
results4 = model4.fit()
results4.summary()

OLSplot.allplots(results4)
plt.show()
plt.close()

##the diagnostics for those models don't look great, but model4 is the better
##of the 2 according to R^2; let's look at the fit:

plt.scatter(np.log(np.abs(xy_data.xp)), np.log(np.abs(xy_data.yp)))
plt.axline((0,0), slope=results4.params[0], color = 'red')
plt.show()
plt.close()

##clearly we are missing the cluster of data at the upper end;
##let's subset the data to try and improve our fit in this region

model5 = smf.ols('np.log(np.abs(yp)) ~ np.log(np.abs(xp)) - 1', data=xy_data[xy_data.xp > 2])
results5 = model5.fit()
results5.summary()

OLSplot.allplots(results5)
plt.show()
plt.close()

#our diagnostics are much better!
#let's look at the fit
plt.scatter(np.log(np.abs(xy_data.xp)), np.log(np.abs(xy_data.yp)))
plt.axline((0,0), slope=results4.params[0], color = 'red')
plt.axline((0,0), slope=results5.params[0], color = 'blue')
plt.show()
plt.close()

#we now do a much better job of hitting the cloud at the top of the data range
#if we back transform our model, we fit something like:
# y = 4 + abs(x-2)^beta
#let's compare!

x_pred = np.arange(0,10,0.01)
y_pred = 4 + np.abs(x_pred - 2) ** results5.params[0]
plt.scatter(x,y)
plt.plot(x_pred, y_pred, color = 'red')
plt.show()
plt.close()

#what is the RSS for this model at the original scale?
np.sum((4 + np.abs(x - 2) ** results5.params[0] - y) ** 2)

### Here are couple of more direct models:

model6 = smf.ols('y ~ np.power(x,2) + x', data=pd.DataFrame(data = {'x':x, 'y':y}))
results6 = model6.fit()
results6.summary()
results6.ssr

#as an offset... no parameter is estimated for x^2
model7 = smf.glm('y ~ x', data=pd.DataFrame(data = {'x':x, 'y':y}), offset = np.power(x,2))
results7 = model7.fit()
results7.summary()
np.sum(results7.resid_working ** 2)

