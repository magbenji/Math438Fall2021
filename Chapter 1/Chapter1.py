import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def recur(f, f0, k, verbose = False, values = False):
  
  result = [None] * (k + 1) #initialize k+1 vector
  result[0] = f0
  for i in range(0, k): result[i+1] = f(result[i]) 
  if(verbose): print(result)
  if(values): return(result)
  return result[k]

def myfun(x):
  return x*2
  
recur(myfun, 2, 10)
recur(myfun, 2, 10, verbose=True)
recur(myfun, 2, 10, values=True)


def example_1_2_5(t, k, Ta):   
  return t + k*(Ta - t)

k = np.exp(np.linspace(np.log(0.01), np.log(0.1), 6))
Ta = np.linspace(60, 80, 6)


allData = pd.DataFrame(columns=['rate','Ta','Time','temp'])



for rate in k:
  for ta in Ta:
    tempVals = recur(lambda x: example_1_2_5(x, rate, ta), 40, 100, values=True)
    tempVals.pop(0)
    rateData = {'rate': rate, 
                'Ta': ta, 
                'Time': np.arange(1,101,1), 
                'temp': tempVals
                  }
    rateData = pd.DataFrame(rateData)
    allData = allData.append(rateData, ignore_index=True)
    

allData[(allData['rate']==k[0]) & (allData['Ta'] == Ta[0])] #note parentheses around each condition

plt.figure()
ax = plt.subplot()

for rate in k:
  for ta in Ta:
    ax.plot('Time', 'temp', 
    data = allData[(allData['rate']==rate) & (allData['Ta'] == ta)],
    label = "Rate = " + str(round(rate,3)) + ", Ambient = " + str(ta))
    
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.set_title('Changes in Temperature over Time,\nAmbient Temperature, and Rate')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(bbox_to_anchor=(1.05, 1.2), loc='upper left', prop={'size': 6})
plt.show()
plt.close()

