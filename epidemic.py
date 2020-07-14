"""
Epidemic/Pandemic spread simulation
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt


# ------------------------------------------------------------
global day, s
# create a figure object and axes
fig = plt.figure()
fig.subplots_adjust(left=0.0, right=0.8, bottom=0, top=1)
ax = fig.add_subplot(
    111, aspect="equal", autoscale_on=False, xlim=(-33.2, 33.2), ylim=(-32.4, 32.4)
)

# set bounds for the box
bounds = [-20, 20, -20, 20]

# rect is the box edge
rect = plt.Rectangle(
    bounds[::2],
    bounds[1] - bounds[0],
    bounds[3] - bounds[2],
    ec="none",
    lw=2,
    fc="none",
)
ax.add_patch(rect)

rect1 = plt.Rectangle(
    (0.2, 0.75), 0.4, 0.15, ec="none", alpha=0.3, label="day", fc="none"
)
ax.add_patch(rect1)

n = 100
person = np.ones(
    n,
    dtype=[
        ("position", float, 2),
        ("velocity", float, 2),
        ("status", float, 1),
        ("size", float, 1),
        ("growth", float, 1),
        ("color", float, 4),
        ("facecolor", float, 4),
    ],
)


# initialize position, velocity, status, growth, color and facecolor

person["position"] = np.random.uniform(-18, 18, size=(n, 2))
person["velocity"] = (-0.5 + np.random.random((n, 2))) * 10
person["growth"] = np.random.uniform(1, 10, n)
person["color"] = np.zeros((n, 4))
person["color"][:, 1] = 0.5
person["color"][0] = [1.0, 0.0, 0.0, 1.0]
person["facecolor"] = np.zeros((n, 4))
person["facecolor"][0] = [1.0, 0.0, 0.0, 0.6]

person["position"][0] = [0.0, 0.0]
person["status"][0] = 0


day = 0
s = np.ones((n)) * 20
text = ax.text(-10, 22, 0)

# create a scatter plot
scat = ax.scatter(
    person["position"][:, 0],
    person["position"][:, 1],
    lw=0.5,
    s=s,
    norm=plt.Normalize(vmin=0, vmax=1),
    label="day",
    edgecolors=person["color"],
    facecolors=person["facecolor"],
)
# legend = ax.legend()


# Animation update function
def update(frame_number):

    current_index = frame_number % n

    global categories, rect, dt, ax, fig, colormap, legend, s

    day = int(frame_number / 30)
    dt = 1 / 30  # 30fps
    infection_radius = 0.4
    social_distancing = 0.0

    # update location
    person["position"] += dt * person["velocity"]
    scat.set_offsets(person["position"])
    # print(person['velocity'])
    # check for crossing boundary

    crossed_x1 = person["position"][:, 0] < bounds[0] + person["size"]
    crossed_x2 = person["position"][:, 0] > bounds[1] - person["size"]
    crossed_y1 = person["position"][:, 1] < bounds[2] + person["size"]
    crossed_y2 = person["position"][:, 1] > bounds[3] - person["size"]

    # find pairs of person undergoing a interaction and update health status, facecolor,
    D = squareform(pdist(person["position"]))
    ind1, ind2 = np.where(D < (infection_radius))
    unique = ind1 < ind2
    ind1 = ind1[unique]
    ind2 = ind2[unique]

    # update edgecolor and facecolor of interacting persons
    for i1, i2 in zip(ind1, ind2):
        if person["status"][i1] == person["status"][i2]:
            continue
        elif person["status"][i1] == 0:
            person["status"][i2] = np.random.choice(
                [0, 1], p=[1 - social_distancing, social_distancing]
            )
            if person["status"][i2] == 0:
                person["color"][i2][0] = 1
                person["color"][i2][1] = 0
                person["facecolor"][i2][0] = 1
                person["facecolor"][i2][3] = 0.5
        elif person["status"][i2] == 0:
            person["status"][i1] = np.random.choice(
                [0, 1], p=[1 - social_distancing, social_distancing]
            )
            if person["status"][i1] == 0:
                person["color"][i1][0] = 1
                person["color"][i1][1] = 0
                person["facecolor"][i1][0] = 1
                person["facecolor"][i1][3] = 0.5

    active_infections = (person["status"] == 0).sum()

    # update size of particles with status = 0
    s = np.where(person["status"] == 0, s + 8, s)
    s = np.where(s > 100, 20, s)

    # update alpha value as function of size
    person["color"][:, 3] = np.where(person["status"] == 0, (1 - (s - 20) / 80), 1)

    # Update velocity of particles at the boundary
    person["velocity"][crossed_x1 | crossed_x2, 0] *= -1
    person["velocity"][crossed_y1 | crossed_y2, 1] *= -1

    # use set function to change color and sizes
    rect.set_edgecolor("k")
    scat.set_facecolor(person["facecolor"])
    scat.set_edgecolors(person["color"])
    scat.set_sizes(s)
    text.set_position((-15, 22))
    text.set_text(f"Day = {day}   Active infections = {active_infections}")

    return scat


# Construct the animation, using the update function as the animation
# director.
animation = animation.FuncAnimation(fig, update, interval=20)

plt.show()
