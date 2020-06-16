# point hopper

import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import math




        

def hop(x0, x1):

    if x1 > 0:
        
        if abs(x0-x1) <= 2:
            x1 = 0.5
            return x1

        if abs(x0-x1) <= 5:
            x1 = x1 - 2
        # if x1 <4:
        #     x1 = x0
        #     return x1
        else:
            x1 = x1 - 5
    
        return x1

    if x1 < 0:
        if abs(x0-x1) <= 2:
            x1 = 0.5
            return x1

        if abs(x0-x1) <= 5:
            x1 = x1 + 1
        # if x1 > -4:
        #     x1 = x0
        #     return x1
        else:
            x1 = x1 + 5

        return x1




def hopr(x0, x1):

    if x0 > 0:

        if abs(x0-x1) <= 10:
            x1 = x1 + 4
        else:
            x1 = x1 + 4
    
        return x1
        

    if x0 < 0:

        if abs(x0-x1) <= 10:
            x1 = x1 - 4
        else:
            x1 = x1 - 4
                
        return x1
       
    if x0 == 0:
        return x1




def linehop(x0,y0, x1, y1):
    d = math.sqrt((x0-x1)**2 + (y0-y1)**2)
    if d >10:
        d1 = d-10
        x = d1 *(x1-x0)/d
        y = d1 * (y1-y0)/d

        return x,y
    
    if d <=10:
        d1 = d-4
        x = d1 *(x1-x0)/d
        y = d1*(y1-y0)/d
        return x, y

def linehop_q(x0,y0,x1,y1):
    d = math.sqrt((x0-x1)**2 + (y0-y1)**2)
    if d >15:
        d1 = d-30
    else:
        d1 = d-15
    
    if abs(x0 > x1):
        x = x0 - d1 *(x0 - x1)/d
    
    else:
        x = x1

    if y1 < y0:
        y = y0 - d1 *(y0 - y1)/d
    else:
        y = y1

    return x, y



def rect(bounds):
    return plt.Rectangle(bounds[::2],
                     bounds[1] - bounds[0],
                     bounds[3] - bounds[2],
                     ec='none', lw=2, fc='none')