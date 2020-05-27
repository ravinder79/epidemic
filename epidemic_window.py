"""
Epidemic/Pandemic spread simulation. Adding another window to visualize total infected and healthy population.
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt



#------------------------------------------------------------
global day, s, x,y
#create a figure object and axes
fig = plt.figure()
#plt.tight_layout()
#fig.subplots_adjust(left=0, right=1.0, bottom=0, top=1)
ax1 = fig.add_subplot(121)
# aspect='equal', autoscale_on=True)
                    # xlim=(-33.2, 33.2), ylim=(-32.4, 32.4))
ax2 = fig.add_subplot(122)
#, aspect='equal', autoscale_on=True)
# set bounds for the box

bounds = [-100, 100, -100, 100]
ax1.axis('off')

bounds1 = [0, 0, 1]
#plt.axis('off')
#rect is the box edge
rect = plt.Rectangle(bounds[::2],
                     bounds[1] - bounds[0],
                     bounds[3] - bounds[2],
                     ec='none', lw=2, fc='none')
ax1.add_patch(rect)
# rect1 = plt.Rectangle((0.2, 0.75), 0.4, 0.15, ec = 'none', alpha=0.3, label = 'day', fc = 'none')
# ax.add_patch(rect1)

n = 150
person = np.ones(n, dtype=[('position', float, 2), ('velocity', float, 2),
                                      ('status',    float, 1),('size',    float, 1),('growth',    float, 1),('color',    float, 4), ('facecolor',    float, 4)])


#initialize position, velocity, status, growth, color and facecolor

person['position'] = np.random.uniform(-40,40, size = (n, 2))
person['velocity'] = (-0.5 + np.random.random((n, 2))) * 50
person['growth'] = np.random.uniform(1, 10, n)
person['color'] = np.zeros((n,4))
person['color'][:,1] = 0.5
person['color'][0] = [1.0, 0.0, 0.0, 1.0]
person['facecolor'] = np.zeros((n,4))
person['facecolor'][0] = [1.0, 0.0, 0.0, 0.6]

person['position'][0] = [0.0 , 0.0]
person['status'][0] = 0


day = 0
x = [0]
y= [1]
s= np.ones((n)) * 20
text = ax1.text(-10,22,0)

#create a scatter plot
scat = ax1.scatter(person['position'][:,0], person['position'][:,1],
        lw=0.5, s = s, label = 'day', edgecolors= person['color'],facecolors=person['facecolor'])

#scat1, = ax2.plot(x,y,marker='o',color="r")


#Animation update function
def update(frame_number):
    
    current_index = frame_number % n

    global categories, rect, dt, ax, fig, colormap, legend, s
    
    
    day = int(frame_number/20) 
    dt = 1 / 30 # 30fps
    infection_radius = 2.0
    social_distancing = 0.0

    # update location
    person['position'] += dt * person['velocity']
    scat.set_offsets(person['position'])
    
    # check for crossing boundary
   
    crossed_x1 = person['position'][:, 0] < bounds[0] + person['size']
    crossed_x2 = person['position'][:, 0] > bounds[1] - person['size']
    crossed_y1 = person['position'][:, 1] < bounds[2] + person['size']
    crossed_y2 = person['position'][:, 1] > bounds[3] - person['size']

    # find pairs of person undergoing a interaction and update health status, facecolor,
    D = squareform(pdist(person['position']))
    ind1, ind2 = np.where(D < (infection_radius))
    unique = (ind1 < ind2)
    ind1 = ind1[unique]
    ind2 = ind2[unique]

    # update edgecolor and facecolor of interacting persons
    for i1, i2 in zip(ind1, ind2):
        if person['status'][i1] == person['status'][i2]:
            continue 
        elif person['status'][i1] == 0:
            person['status'][i2] = np.random.choice([0,1],p =[1-social_distancing, social_distancing])
            if person['status'][i2] == 0:
                person['color'][i2][0] = 1
                person['color'][i2][1] = 0
                person['facecolor'][i2][0] = 1
                person['facecolor'][i2][3] = 0.5
        elif person['status'][i2] == 0:
            person['status'][i1] = np.random.choice([0,1],p = [1-social_distancing, social_distancing])
            if person['status'][i1] == 0:
                person['color'][i1][0] = 1
                person['color'][i1][1] = 0
                person['facecolor'][i1][0] = 1
                person['facecolor'][i1][3] = 0.5


    active_infections = (person['status']==0).sum()
   
    # update size of particles with status = 0
    s = np.where(person['status'] ==0, s+8, s)
    s = np.where(s > 100, 20, s)
    
    #update alpha value as function of size
    person['color'][:, 3] = np.where(person['status'] ==0, (1-(s-20)/80), 1)

    #Update velocity of particles at the boundary
    person['velocity'][crossed_x1 | crossed_x2, 0] *= -1
    person['velocity'][crossed_y1 | crossed_y2, 1] *= -1
    
    
    
    # use set function to change color and sizes
    rect.set_edgecolor('k')
    scat.set_facecolor(person['facecolor'])
    scat.set_edgecolors(person['color'])
    scat.set_sizes(s)
    text.set_position((-15,22))
    text.set_text(f'Day = {day}   Active infections = {active_infections}')


    x.append(day)
    y.append(active_infections/150*100)
    #scat1.set_data(x, y)s
    #scat1 = ax2.plot(x[day],y[day],marker='o',color="r")
    ax2.clear()
    ax2.plot(x,y)
    #plt.xlim(0,50)
    plt.ylim(0,100)
    return scat,


# Construct the animation, using the update function as the animation
# director.
animation = animation.FuncAnimation(fig, update, interval=20)

plt.show()



