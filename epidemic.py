"""
Epidemic/Pandemic spread simulation
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt



#------------------------------------------------------------
global day
#create a figure object and axes
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

# set bounds for the box
bounds = [-2, 2, -2, 2]

# rect is the box edge
rect = plt.Rectangle(bounds[::2],
                     bounds[1] - bounds[0],
                     bounds[3] - bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(rect)

rect1 = plt.Rectangle((0.2, 0.75), 0.4, 0.15, ec = 'none', alpha=0.3, label = 'day', fc = 'none')
ax.add_patch(rect1)

n = 100
person = np.ones(n, dtype=[('position', float, 2), ('velocity', float, 2),
                                      ('status',    float, 1),('size',    float, 1)])
person['position'] = np.random.uniform(-2,2, size = (n, 2))
#person['position'] = -0.5 + np.random.random((n, 2)) 
person['velocity'] = (-0.5 + np.random.random((n, 2))) * 1.5
person['status'][0] = 0

person['size'] = 0.04
categories = np.array([1] * n)
categories[0] = 0.00
day = 0
cmap = np.array(['r', 'g'])
size = 20
#color_data = categories
# Construct the scatter plot which we will update during animation
scat = ax.scatter(person['position'][:,0], person['position'][:,1],
                  lw=0.5,  c= person['status'], s = 30, norm = plt.Normalize(vmin=0, vmax=1),
            cmap = "bwr_r", label = 'day')
legend = ax.legend()


def update(frame_number):
    
    
    global categories, rect, dt, ax, fig, colormap, legend
    day = int(frame_number/30)
    
    dt = 1 / 30 # 30fps
    person['position'] += dt * person['velocity']

    scat.set_offsets(person['position'])
    # check for crossing boundary
   
    crossed_x1 = person['position'][:, 0] < bounds[0] + person['size']
    crossed_x2 = person['position'][:, 0] > bounds[1] - person['size']
    crossed_y1 = person['position'][:, 1] < bounds[2] + person['size']
    crossed_y2 = person['position'][:, 1] > bounds[3] - person['size']

    # find pairs of particles undergoing a collision
    D = squareform(pdist(person['position']))
    ind1, ind2 = np.where(D < (2 * person['size']))
    unique = (ind1 < ind2)
    ind1 = ind1[unique]
    ind2 = ind2[unique]

    for i1, i2 in zip(ind1, ind2):
        if person['status'][i1] == 0:
            person['status'][i2] = 0
        if person['status'][i2] == 0:
            person['status'][i1] = 0

    for i in range (0, n):
        categories[i] = person['status'][i]
   
    person['velocity'][crossed_x1 | crossed_x2, 0] *= -1
    person['velocity'][crossed_y1 | crossed_y2, 1] *= -1
    rect.set_edgecolor('k')
   
    scat.set_array(person['status'])
    scat.set_label(day)
    legend.remove()
    legend = plt.legend( loc='upper left')
    # red_patch = mpatches.Patch( label='day')
    # plt.legend(handles=[red_patch])
    

    return scat, [legend]
# Construct the animation, using the update function as the animation
# director.
animation = animation.FuncAnimation(fig, update, interval=20)
plt.show()



