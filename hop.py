# point hopper

import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import math




        

def hop(x0, x1):

    if x1 > 0:

        if abs(x0-x1) <= 10:
            x1 = x1 - 4
        else:
            x1 = x1 - 15
    
        return x1

    if x1 < 0:

        if abs(x0-x1) <= 10:
            x1 = x1 + 4
        else:
            x1 = x1 + 15

        return x1




def hopr(x0, x1):

    if x0 > 0:

        if abs(x0-x1) <= 10:
            x1 = x1 + 4
        else:
            x1 = x1 + 15
    
        return x1

    if x0 < 0:

        if abs(x0-x1) <= 10:
            x1 = x1 - 4
        else:
            x1 = x1 - 15

        return x1
