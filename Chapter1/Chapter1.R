recur <- function(f,f0,k,verbose=F,values = F){
  ret <- rep(NA,k+1)
  ret[1] <- f0
  for(i in 2:(k+1)) ret[i] <- f(ret[i-1])
  if(verbose) print(ret)
  if(values) return(ret)
  ret[k+1]
}

myfun <- function(x) x * 2

recur(myfun, 2, 10)
recur(myfun, 2, 10, verb=T)
recur(myfun, 2, 10, val=T)


###----------Example 1.2.5: Heat Transfer

# ∆t = k(T - t)
# t0 = 40
# Ta is the ambient temperature

example_1_2_5  <- function(t, k, Ta) t + k*(Ta - t)

### Vary k and Ta across 6 different levels and plot solutions
### Vary k from 0.01 to 0.1 at the log-scale; Vary Ta from 60 to 80 
### Plot 100 time points
### Create plots based each level of k (i.e., 6 lines per plot)
### With the unique plots for each k, create a large plot with 6 facets 

### Commands needed: exp(), log(), seq(), rep(), ggplot()+++, rbind(),

k <- exp(seq(log(0.01), log(0.1), length=6))
Ta <- seq(60, 80, length = 6)


library(ggplot2)

allData <- data.frame(rate = 0, Ta = 0, Time = 0, temp = 0)
allData <- allData[0,]

for(rate in k){
  rateData <- data.frame(Ta = 0, Time = 0, temp=0)
  rateData <- rateData[0,]
  for(ta in Ta){
    rateData <- rbind(rateData, 
                      data.frame(
                        Ta = rep(ta, 100),
                        Time = 1:100,
                        temp = recur(function(x) example_1_2_5(x, rate, ta), 40, 100, val= T)[-1]
                      )
                      )
  }
  g <- ggplot(rateData, aes(x=Time, y=temp, group = Ta, color = Ta))
  g <- g + geom_line() + theme_bw() + ylab("Temperature") + 
          scale_color_gradient(name="Ambient\nTemperature", low="darkblue", high="red") + 
          ggtitle(paste("Rate =", round(rate,3), sep=" "))
  print(g)
  rateData$rate = rate
  allData <- rbind(allData, rateData)
}

g <- ggplot(allData, aes(x=Time, y=temp, group = Ta, color = Ta))

g + geom_line() + theme_bw() + ylab("Temperature") + 
  scale_color_gradient(name="Ambient\nTemperature", low="darkblue", high="red") + 
  ggtitle("Changes in Temperature over Time, Ambient Temperature, and Rate") + 
  facet_wrap(vars(rate), labeller = labeller(rate = function(x) paste("k = ", round(as.numeric(x),3), sep="")))

