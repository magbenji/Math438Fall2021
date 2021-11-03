import plotnine as p9
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### A plot of a linear program system
#  This would be for a system given by:
#
#  Maximize 2*x + 3*y
#  Subject to
#    x >= 0 
#    y >= 0
#    2*x + 3*y >= 6
#    3*x - y <= 15  (or -3*x + y >= -15)
#    x - y >= -4
#    2*x + 5*y <= 27 (or -2*x - 5*y >= -27)


#make up some data to create contours to visualize objective function
data = pd.merge(pd.DataFrame({'x': np.linspace(0,7,50), 'key':1}), pd.DataFrame({'y': np.linspace(0,7,50), 'key':1}), on="key").drop("key", 1)
data['z'] = 2*data.x + 3*data.y  #this would be the function to maximize/minize; here 2*x + 3*y

#Used to color the polygon showing the feasible space.
#The point I'm putting in for x,y coordinates are based on intersections (extreme points)
#of the constraints.
shadeMe = pd.DataFrame({'x':[3,5,6,1,0,0], 'y':[0,0,3,5,4,2]})

#sadly, plotnine has no geom_contour, swo we have to find a kludge


#kludge 1: use stat_function to draw individual contours; args = {'k': VALUE} gives the k = VALUE contour
#NB: I had to solve for the contour function by solving k = 2*x + 3*y... cf line 6.
#Everything with a call to geom_abline, geom_hline, or geom_vline is defining/plotting a constraint
countourK = lambda x,k: -1/3*(2*x - k)
(
  p9.ggplot(data, p9.aes(x='x',y='y')) + p9.stat_function(fun = countourK, args = {'k':2}, linetype = 'dashed', color = "blue")
  + p9.stat_function(fun = countourK, args = {'k':6}, linetype = 'dashed', color = "blue") 
  + p9.stat_function(fun = countourK, args = {'k':10}, linetype = 'dashed', color = "blue") 
  + p9.stat_function(fun = countourK, args = {'k':14}, linetype = 'dashed', color = "blue") 
  + p9.stat_function(fun = countourK, args = {'k':18}, linetype = 'dashed', color = "blue") 
  + p9.stat_function(fun = countourK, args = {'k':22}, linetype = 'dashed', color = "blue")
  + p9.stat_function(fun = countourK, args = {'k':26}, linetype = 'dashed', color = "blue")
  + p9.geom_abline(mapping=p9.aes(intercept = 2, slope = -2/3), color = "red")
  + p9.geom_hline(mapping=p9.aes(yintercept = 0 ), color="red") 
  + p9.geom_vline(mapping=p9.aes(xintercept = 0), color="red")
  + p9.geom_abline(mapping=p9.aes(intercept = -15, slope = 3), color="red") 
  + p9.geom_abline(mapping=p9.aes(intercept = 4, slope = 1), color="red")
  + p9.geom_abline(mapping=p9.aes(intercept = 27/5, slope = -2/5), color="red")
  + p9.geom_polygon(data = shadeMe, mapping=p9.aes(x='x',y='y'), fill = "gray", alpha = 0.3)
  + p9.theme_bw() + p9.ggtitle("Constrained System with Level Curves") + p9.ylim(0,6)
)

#kludge 2: use maplotlib to draw the contours

myggplot = (
  p9.ggplot(data, p9.aes(x='x',y='y')) 
  + p9.geom_abline(mapping=p9.aes(intercept = 2, slope = -2/3), color = "red")
  + p9.geom_hline(mapping=p9.aes(yintercept = 0 ), color="red") 
  + p9.geom_vline(mapping=p9.aes(xintercept = 0), color="red")
  + p9.geom_abline(mapping=p9.aes(intercept = -15, slope = 3), color="red") 
  + p9.geom_abline(mapping=p9.aes(intercept = 4, slope = 1), color="red")
  + p9.geom_abline(mapping=p9.aes(intercept = 27/5, slope = -2/5), color="red")
  + p9.geom_polygon(data = shadeMe, mapping=p9.aes(x='x',y='y'), fill = "gray", alpha = 0.3)
  + p9.theme_bw() + p9.ggtitle("Constrained System with Level Curves") + p9.ylim(0,6)
)

fig = myggplot.draw()
[ax] = fig.get_axes()
ax.contour(data.x.to_numpy().reshape(50,-1), data.y.to_numpy().reshape(50,-1), data.z.to_numpy().reshape(50,-1), levels=6, linestyles='dashed', linewidths=2)
plt.show()
plt.close('all')
