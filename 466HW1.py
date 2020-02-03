# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from math import *




#################################Yield-to-Maturity############################################

#dictionary in which keys are start day numbers and values are ytm arrays
#one dictionary for each curve we want to make
Y_Arrays = {} 

#split 5 years into 6 month periods
T = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])


#yield values (one array for each start day) corresponding the time to maturity value
#array T above
y2 = np.array([0.009, 0.0073, 0.0076, 0.0072, 0.0075, 0.0072, 0.0072, 0.0071, 0.0079, 0.0071])
y3 = np.array([0.009, 0.0072, 0.0075, 0.0071, 0.0074, 0.007, 0.0071, 0.007, 0.0077, 0.007])
y6 = np.array([0.009, 0.0071, 0.0073, 0.007, 0.0073, 0.007, 0.007, 0.0068, 0.0073, 0.0068]) 
y7 = np.array([0.009, 0.0071, 0.0074, 0.0071, 0.0074, 0.007, 0.0071, 0.007, 0.0075, 0.0069])
y8 = np.array([0.009, 0.0072, 0.0074, 0.0071, 0.0074, 0.007, 0.0071, 0.007, 0.0074, 0.0069])
y9 = np.array([0.009, 0.0073, 0.0076, 0.0072, 0.0075, 0.0071, 0.0072, 0.007, 0.0076, 0.0071])
y10 = np.array([0.009, 0.0075, 0.0076, 0.0072, 0.0075, 0.0072, 0.0072, 0.0071, 0.0076, 0.0071])
y13 = np.array([0.009, 0.0074, 0.0076, 0.0073, 0.0076, 0.0073, 0.0073, 0.0071, 0.0076, 0.0071])
y14 = np.array([0.01, 0.0075, 0.0076, 0.0073, 0.0076, 0.0072, 0.0072, 0.007, 0.0076, 0.007])
y15 = np.array([0.01, 0.0074, 0.0075, 0.0072, 0.0076, 0.0071, 0.0071, 0.007, 0.0075, 0.007])


#iterate through the days
for day in range(2,16):
    
    if (day==4 or day==5 or day==11 or day==12):
        continue
   
    #6 month yields for this day    
    yields = eval("y"+str(day))    
    
    #we wil have a time array for each 6 month period. The corresponding yield 
    #array will be obtained by linearly interpolating between the yield values 
    #at the endpoints of the time array. This will give us 10 pairs of time/yield
    #arrays. They will be placed in the following lists.
    t_arrays = []
    y_arrays = []
    
    
    for i in range(0,9):
        
        t = np.zeros(10+1)
        y = np.zeros(10+1)
        
        t[0] = T[i]
        t[-1] = T[i+1]
        
        for k in range(1, 10):
           t[k]=t[k-1]+((t[-1]-t[0])/10)
        
        
        t_arrays.append(t)
        
       
        y[0]=yields[i]
        y[-1]=yields[i+1]
        
        #slope
        m = (y[-1]-y[0])/(t[-1]-t[0])
        
        for k in range(1, 10):
           y[k]=y[k-1]+m*((t[-1]-t[0])/10)
        
               
        y_arrays.append(y)
        
        
            
    #concatenate all arrays in t_arrays_ytm into 1 (same for y_arrays_atm) to get 5 year
    #time and corresponding ytm arrays for this start day
    for i in range(0,len(t_arrays)):
       if (i==0):
           T_day = t_arrays[i]
           Y_day = y_arrays[i]
       else:
           T_day = np.concatenate([T_day, t_arrays[i]])
           Y_day = np.concatenate([Y_day, y_arrays[i]])
    
    #array that will hold Time-to-maturity, which will be the horizontal axis of all 
    #our plots (do this only once)
    if (day==2):
        T_Array = T_day
        
    Y_Arrays[str(day)]=Y_day
    
    
#plot yield curves
plt.figure(1)
for day in range(2,16):
    
    if (day==4 or day==5 or day==11 or day==12):
        continue
    

    plt.plot(T_Array, Y_Arrays[str(day)], label='Ytm curve for ' + str(day) + '-Jan-2020')

plt.legend(prop={"size":5})  
plt.xlabel('Time to maturity (in years)') 
plt.ylabel('Yield to maturity (in %)')     
plt.title('Yield-to-Maturity vs Time-to-Maturity curve')
##########################################################################################

############################### Forward Rate Curve########################################

#define a list of forward rate matrices for each day (this will be useful later)
f_rates = []

plt.figure(2)
for day in range(2,16):

    if (day==4 or day==5 or day==11 or day==12):
        continue    
    
    #the index for 1 year (and its corresponding ytm) is 11. Here we cut out the
    #first year and its correspoding yields. These will be used for 1 year
    #forward rate calculation    
    yields = Y_Arrays[str(day)][12:]
    time =  T_Array[12:]
    
    #if (day==2):
      #  print time[0], time[20], time[42], time[65], time[86] 
    
    #yield at one year   
    yield_1=Y_Arrays[str(day)][11]
    
    #apply forward rate formula rate formula
    forward_rate=(time*yields-yield_1)/(time-1)
    f_rates.append(forward_rate)    
    
    plt.plot(time, forward_rate, label='Forward Rate for ' + str(day) + '-Jan-2020')

plt.legend(loc='upper center', prop={"size":5})  
plt.xlabel('Time (in years)') 
plt.ylabel('Forward rate (in %)') 
plt.title('1-Year Forward rate curve') 
#########################################################################################

#############################Covariance Matrices#########################################

#let us begin by defining the matrix whose elements are r_{i,j}, as described
#in Q5 in the report. We do this manually

R = np.array([[0.0073,0.0072,0.0071,0.0071,0.0072,0.0073,0.0075,0.0074,0.0075,0.0074]
            ,[0.0072,0.0071,0.007,0.0071,0.0071,0.0072,0.0072,0.0073,0.0073,0.0072]
            ,[0.0072,0.007,0.007,0.007,0.007,0.0071,0.0072,0.0073,0.0072,0.0071]
            ,[0.0071,0.007,0.068,0.007,0.007,0.007,0.0071,0.0071,0.007,0.007]            
            ,[0.0071,0.007,0.068,0.069,0.069,0.0071,0.0071,0.0071,0.007,0.007]])
        
            
#We now compute matrix X, whose elements are X_{i,j}, as defined in Q5
X =np.zeros((5,9))

for i in range(0,5):
    for j in range(0,9):
        X[i][j]=np.log(R[i][j+1]/R[i][j])
   
     
cov_X = np.cov(X)

#we now to the same thing with the one year forward rate
#we define the matrix F, whose elements are f_{i,j}, as defined in Q5
F=np.zeros((5,10))


#In each forward rate matrix (for each start day), looking at the 1-st, 21st, 
#43rd,66th, and 87th elements gives us the 1-1, 1-2, 1-3, 1-4 and 1-5 forward
#rates (these were found by visually inspecting arrays in the code). This is  
#the colum of F corresponding to that day. 
for j in range(0, len(f_rates)):
    T=f_rates[j]    
    F[:,j]=np.array([T[0], T[20], T[42], T[65], T[86]]) 
    
#We now compute matrix Y, whose elements are Y_{i,j}, as defined in Q5
Y =np.zeros((5,9))

for i in range(0,5):
    for j in range(0,9):
        Y[i][j]=np.log(F[i][j+1]/F[i][j])
    
cov_Y=np.cov(Y)
    

