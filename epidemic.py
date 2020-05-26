"""
Epidemic/Pandemic spread simulation
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt



#------------------------------------------------------------
global day, s
#create a figure object and axes
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-33.2, 33.2), ylim=(-32.4, 32.4))

# set bounds for the box
bounds = [-20, 20, -20, 20]

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
                                      ('status',    float, 1),('size',    float, 1),('growth',    float, 1),('color',    float, 4)])
person['position'] = np.random.uniform(-10,10, size = (n, 2))
#person['position'] = -0.5 + np.random.random((n, 2)) 
person['velocity'] = (-0.5 + np.random.random((n, 2))) * 10
person['status'][0] = 0
person['growth'] = np.random.uniform(1, 10, n)
person['color'] = np.zeros((n,4))
person['color'][:,1] = 0.5
# person['color'][:,3] = 0
# categories = np.array([1] * n)
# categories[0] = 0.00
day = 0
#cmap = np.array(['r', 'g'])
s= np.ones((n)) * 10
#color_data = categories
# Construct the scatter plot which we will update during animation
# scat = ax.scatter(person['position'][:,0], person['position'][:,1],
#                   lw=0.5,  c= person['status'], s = person['size'], norm = plt.Normalize(vmin=0, vmax=1),
#             cmap = "bwr_r", label = 'day', alpha = 0.7, edgecolors= person['color'],facecolors='none')

scat = ax.scatter(person['position'][:,0], person['position'][:,1],
        lw=0.5, s = person['size'], norm = plt.Normalize(vmin=0, vmax=1)
            , label = 'day', alpha = 0.7, edgecolors= person['color'],facecolors='none')
legend = ax.legend()


def update(frame_number):
    
    current_index = frame_number % n

    global categories, rect, dt, ax, fig, colormap, legend, s
    day = int(frame_number/30)
    
    dt = 1 / 30 # 30fps
    person['position'] += dt * person['velocity']
    person['color'][:, 3] =  (1.0/50) + person['color'][:, 3]
    # print(person['color'][1])
    person['color'][:,3] = np.clip(person['color'][:,3], 0, 1)
    
    scat.set_offsets(person['position'])
    # check for crossing boundary
   
    crossed_x1 = person['position'][:, 0] < bounds[0] + person['size']
    crossed_x2 = person['position'][:, 0] > bounds[1] - person['size']
    crossed_y1 = person['position'][:, 1] < bounds[2] + person['size']
    crossed_y2 = person['position'][:, 1] > bounds[3] - person['size']

    # find pairs of particles undergoing a collision
    D = squareform(pdist(person['position']))
    #ind1, ind2 = np.where(D < (2 * person['size']))
    ind1, ind2 = np.where(D < (1))

    unique = (ind1 < ind2)
    ind1 = ind1[unique]
    ind2 = ind2[unique]

    for i1, i2 in zip(ind1, ind2):
        if person['status'][i1] == 0:
            person['status'][i2] = 0
            person['color'][i2][0] = 1
           
            person['color'][i2][1] = 0
        if person['status'][i2] == 0:
            person['status'][i1] = 0
            person['color'][i1][0] = 1
            person['color'][i1][1] = 0


    # for i in range(0,n):
    #     if person['status'][i] == 0:
    #         s[i] +=  2
    #     if s[i] >=40:
    #         s[i] = 20
    
    
    s = np.where(person['status'] ==0, s+8, s)
    s = np.where(s > 160, 20, s)
    #print(person['status'])
    print(s)
    person['color'][:, 3] = (s-20)/140
    print(person['color'])
    person['velocity'][crossed_x1 | crossed_x2, 0] *= -1
    person['velocity'][crossed_y1 | crossed_y2, 1] *= -1
    rect.set_edgecolor('k')
   
    scat.set_edgecolors(person['color'])
    scat.set_label(day)
    legend.remove()
    legend = plt.legend( loc='upper left')
    scat.set_sizes(s)
    #scat.set_sizes(person['size'])
    
    # red_patch = mpatches.Patch( label='day')
    # plt.legend(handles=[red_patch])
    

    return scat, [legend]
# Construct the animation, using the update function as the animation
# director.
animation = animation.FuncAnimation(fig, update, interval=20)
plt.show()



