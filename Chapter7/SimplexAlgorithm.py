import numpy as np
import numpy.linalg as la

A = np.array([-2, -3, 1, 0, 0, 0,
                3, -1, 0, 1, 0, 0,
                -1, 1, 0 ,0, 1, 0,
                2, 5, 0, 0, 0, 1]).reshape(4,-1)

c = np.array([2,3,0,0,0,0])
b = np.array([-6,15,4,27])

x = np.array([0,0,-6,15,4,27])


B = np.arange(2,6)
N = np.arange(2)

A[:,B]

Lambda = la.inv(A[:,B].transpose()) @ c[B]
sn = c[N] - A[:,N].transpose() @ Lambda #for maximization: continue as long as max(sn) > 0

enter = N[np.argmax(sn)]  

d = la.inv(A[:,B]) @ A[:,enter]
ratios = x[B]/d #get the ratios for the ratio test

multiplier = np.min(ratios[d>0]) #value of exiting index
Exit = B[ratios==multiplier]

x[enter] = multiplier
x[B] = x[B] - d*multiplier

B = np.union1d(np.setdiff1d(B,Exit),enter)
B.sort()
N = np.setdiff1d(np.arange(A.shape[1]), B)

