"""
Epidemic/Pandemic spread simulation. Added quarantine scenario. 
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math

plt.style.use("dark_background")


# ------------------------------------------------------------
global day, s, x, y, day1, y1
day = 0
day1 = 0
#####
# Global Quarantine Flag##
# 0 for off, 1 for on
quarantine = 0

# quarantine percentage
q = 0.8


# Infection radius:
infection_radius = 0.7

# Social distancing factor: 0- no social distancing, 1: complete distancing
social_distancing = 0.5

# create a figure object and axes
fig = plt.figure(figsize=(14, 6))
plt.rcParams["figure.facecolor"] = "black"
gs1 = fig.add_gridspec(nrows=6, ncols=6)
ax1 = fig.add_subplot((gs1[:, 0:4]), aspect="equal")
ax1.axis("off")


ax2 = fig.add_subplot(gs1[1:5, 3:6])
ax2.set_facecolor("gray")


# This helps in getting rid of margins on side of axes. Default is 5%
plt.rcParams["axes.xmargin"] = 0.0

# set bounds for the 'box'
bounds = [-100, 100, -100, 100]
bounds3 = [-20, 20, -150, -110]

# rect is the box edge
rect = plt.Rectangle(
    bounds[::2],
    bounds[1] - bounds[0],
    bounds[3] - bounds[2],
    ec="none",
    lw=2,
    fc="none",
)
ax1.add_patch(rect)
rect1 = plt.Rectangle(
    bounds3[::2],
    bounds3[1] - bounds3[0],
    bounds3[3] - bounds3[2],
    ec="none",
    lw=2,
    fc="none",
)
ax1.add_patch(rect1)

n = 500
person = np.ones(
    n,
    dtype=[
        ("position", float, 2),
        ("velocity", float, 2),
        ("status", int, 1),
        ("qtflag", int, 1),
        ("duration", float, 1),
        ("size", float, 1),
        ("color", float, 4),
        ("facecolor", float, 4),
    ],
)

# Status definitions:
# 0: Infected
# 1: suseptible
# 2: Recovered/Removed


# initialize position, velocity, status, color and facecolor

person["position"] = np.random.uniform(-70, 70, size=(n, 2))
person["velocity"] = (-0.5 + np.random.random((n, 2))) * 50
person["color"] = np.zeros((n, 4))
person["color"][:, 1] = 0.5
person["color"][0] = [1.0, 0.0, 0.0, 1.0]
person["facecolor"] = np.zeros((n, 4))
person["facecolor"] = [0, 0.55, 0.52, 1.0]  # Set color to 'teal with alpha = 1.0

# initialize first infected person
person["facecolor"][0] = [1.0, 0.0, 0.0, 0.6]
person["position"][0] = [0.0, 0.0]
person["status"][0] = 0
person["duration"] = 0.0
person["qtflag"] = 0


day = 0
day1 = 0.00
x = [0]
y = [0]
y1 = [100]
s = np.ones((n)) * 3
text1 = ax1.text(-10, 42, "")
text2 = ax1.text(-10, 100, "")
text3 = ax1.text(-10, 42, "")
text4 = ax1.text(-10, 100, "", fontsize=16)


# create a scatter plot
scat = ax1.scatter(
    person["position"][:, 0],
    person["position"][:, 1],
    lw=0.5,
    s=s,
    label="day",
    edgecolors=person["color"],
    facecolors=person["facecolor"],
)

(line1,) = ax2.plot(x, y)
(line2,) = ax2.plot(x, y1)

# Animation update function
def update(frame_number):

    global rect, dt, ax, fig, colormap, legend, s, day, day1

    day = int(frame_number / 20)
    day1 = frame_number / 20
    # print(day1)
    dt = 1 / 30  # 30fps
    # infection_radius = 0.8
    # social_distancing = 0.0

    # update location

    for i in range(n):
        if (person["qtflag"][i] != 2) and person["position"][i][1] > -100:
            person["position"][i][0] += dt * person["velocity"][i][0]
            person["position"][i][1] += dt * person["velocity"][i][1]

    scat.set_offsets(person["position"])

    crossed_x1 = (person["position"][:, 0] < bounds[0] + person["size"] + 3) & (
        person["qtflag"] != 2
    )
    crossed_x2 = (person["position"][:, 0] > bounds[1] - person["size"] - 3) & (
        person["qtflag"] != 2
    )
    crossed_y1 = (person["position"][:, 1] < bounds[2] + person["size"] + 3) & (
        person["qtflag"] != 2
    )
    crossed_y2 = (person["position"][:, 1] > bounds[3] - person["size"] - 3) & (
        person["qtflag"] != 2
    )

    # Update velocity for persons at boundary to avoid going out of box
    person["velocity"][crossed_x1 | crossed_x2, 0] *= -1
    person["velocity"][crossed_y1 | crossed_y2, 1] *= -1

    # find pairs of person undergoing a interaction and update health status, facecolor,
    D = squareform(pdist(person["position"]))
    ind1, ind2 = np.where(D < (infection_radius))
    unique = ind1 < ind2
    ind1 = ind1[unique]
    ind2 = ind2[unique]

    # update status, edgecolor and facecolor of interacting persons
    for i1, i2 in zip(ind1, ind2):
        if (person["status"][i1] == person["status"][i2]) & (
            person["position"][i1][1] < -105
        ):
            continue
        elif person["status"][i1] == 0:
            person["status"][i2] = np.random.choice(
                [0, 1], p=[1 - social_distancing, social_distancing]
            )
            if person["status"][i2] == 0:
                person["color"][i2][0] = 1
                person["color"][i2][1] = 0
                person["facecolor"][i2] = [1, 0, 0, 0.6]
                person["qtflag"][i2] = np.random.choice(
                    [0, 1], p=[0.1, 0.9]
                )  # quarantine flag

        elif person["status"][i2] == 0:
            person["status"][i1] = np.random.choice(
                [0, 1], p=[1 - social_distancing, social_distancing]
            )
            if person["status"][i1] == 0:
                person["color"][i1][0] = 1
                person["color"][i1][1] = 0
                person["facecolor"][i1] = [1, 0, 0, 0.6]
                person["qtflag"][i1] = np.random.choice(
                    [0, 1], p=[1 - q, q]
                )  # quarantine flag

    # Used to turn on/off quarantine
    if quarantine == 0:
        person["qtflag"] = 0

    active_infections = (person["status"] == 0).sum()
    infected_pcnt = int(active_infections / n * 100)
    recovered = (person["status"] == 2).sum()
    recovered_pcnt = int(recovered / n * 100)
    quarantined = (person["qtflag"] == 2).sum()

    # update infection duration of person
    person["duration"] = np.where(
        person["status"] == 0, person["duration"] + 0.05, person["duration"]
    )

    # Introducing quarantine.
    stepx = 15
    stepy = 15
    for i in range(
        len(
            (person["qtflag"] == 1)
            & (person["position"][:, 1] >= -100)
            & (person["duration"] > 1)
        )
    ):
        if (
            (person["qtflag"][i] == 1)
            & (person["position"][i][1] >= -100)
            & (infected_pcnt + recovered_pcnt > 10)
            & (person["duration"][i] > 1)
        ):
            person["qtflag"][i] = 2

    ls = np.where((person["qtflag"] == 2) & (person["status"] == 0))
    ls = ls[0]

    for i in ls:

        if (person["position"][i][0]) > 10:
            person["position"][i][0] = person["position"][i][0] - stepx
        if (person["position"][i][0]) < -10:
            person["position"][i][0] = person["position"][i][0] + stepx
        if person["position"][i][1] > (-130):
            person["position"][i][1] = person["position"][i][1] - stepy

    # update size of particles with status = 0
    s = np.where(person["status"] == 0, s + 4, s)
    s = np.where(s > 20, 3, s)
    s = np.where(person["status"] == 2, 8, s)
    s = np.where(person["qtflag"] == 1, 8, s)

    # Update status of person when infection duration > 15 days
    person["status"] = np.where(person["duration"] > 15, 2, person["status"])

    total_infections_pct = int(
        (((person["status"] == 0) + (person["status"] == 2)).sum()) / n * 100
    )
    # return of quarantined persons who have recovered after 21 days
    lsq = np.where((person["qtflag"] == 2) & (person["status"] == 2))
    lsq = lsq[0]

    for i in lsq:
        if person["position"][i][1] < (-100.5):
            person["position"][i][1] = person["position"][i][1] + 25
        if person["position"][i][1] >= -100.5:
            person["qtflag"][i] = 0
        else:
            continue

    # update alpha value as function of size
    person["color"][:, 3] = np.where(person["status"] == 0, (1 - (s - 3) / 17), 1)

    # changing edgecolor of persons with status =2 (recovered/removed)
    person["color"][:, 2] = np.where(person["status"] == 2, 0.5, person["color"][:, 2])
    person["color"][:, 1] = np.where(person["status"] == 2, 0.5, person["color"][:, 1])
    person["color"][:, 0] = np.where(person["status"] == 2, 0.5, person["color"][:, 0])

    # changing color of persons with status =2 (recovered/removed)
    person["facecolor"][:, 2] = np.where(
        person["status"] == 2, 0.5, person["facecolor"][:, 2]
    )
    person["facecolor"][:, 1] = np.where(
        person["status"] == 2, 0.5, person["facecolor"][:, 1]
    )
    person["facecolor"][:, 0] = np.where(
        person["status"] == 2, 0.5, person["facecolor"][:, 0]
    )

    # use set function to change color and sizes
    rect.set_edgecolor("w")
    rect1.set_edgecolor("r")
    scat.set_facecolor(person["facecolor"])
    scat.set_edgecolors(person["color"])
    scat.set_sizes(s)
    text1.set_position((-55, 105))
    text1.set_text(f"Day = {day}   Active infections = {active_infections}")

    # Plotting second subplot ax2
    x.append(day1)
    y.append(active_infections / n * 100)
    y1.append(100 - (recovered / n * 100))
    ax2.clear()
    line1.set_data(x, y)
    p = ax2.fill_between(x, y, y2=0, color="red", alpha="0.5")
    p1 = ax2.fill_between(x, y1, y2=100, color="gray", alpha="0.5")
    p2 = ax2.fill_between(x, y, y1, color="teal", alpha="0.5")

    line2.set_data(x, y1)
    ax2.set_ylim(ymin=0, top=100)
    ax2.set_xlim([0, day1])
    text2.set_position((200, 75))
    text2.set_text(
        f"Infected = {infected_pcnt}%   Removed/Recovered = {recovered_pcnt}%"
    )
    text3.set_position((-50, -160))
    text3.set_text(f"Total Quarantined = {quarantined}")
    text4.set_position((220, 95))
    text4.set_text(f"Total Infections = {total_infections_pct}%")

    return scat, line1, p, p1, p2


# Construct the animation, using the update function as the animation
# director.
anim = animation.FuncAnimation(fig, update, interval=10, frames=1400)

# save command below
# anim.save('epidemic_q80.mp4', fps = 15.0, dpi=600)
plt.show()
