library(ggplot2)

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
data <- merge(data.frame(x=seq(0,7,length=50)), data.frame(y=seq(0,5,length=50)))
data$z <- 2*data$x + 3*data$y #this would be the function to maximize/minize; here 2*x + 3*y

#Used to color the polygon showing the feasible space.
#The point I'm putting in for x,y coordinates are based on intersections (extreme points)
#of the constraints.
shadeMe <- data.frame(x=c(3,5,6,1,0,0),y=c(0,0,3,5,4,2))

#Everything with a call to geom_abline, geom_hline, or geom_vline is defining/plotting a constraint
ggplot(data, aes(x,y)) + geom_contour(aes(z=z), bins = 10, linetype =2) + geom_abline(aes(intercept = 2, slope = -2/3), col="red") + 
  geom_hline(aes(yintercept = 0 ), col="red") + 
  geom_vline(aes(xintercept = 0), col="red") + 
  geom_abline(aes(intercept = -15, slope = 3), col="red") + 
  geom_abline(aes(intercept = 4, slope = 1), col="red") + 
  geom_abline(aes(intercept = 27/5, slope = -2/5), col="red") + 
  geom_polygon(data = shadeMe, aes(x,y), fill = "gray", alpha = 0.3) +
  theme_bw() + ggtitle("Constrained System with Level Curves")