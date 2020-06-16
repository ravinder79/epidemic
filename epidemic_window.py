"""
Epidemic/Pandemic spread simulation. Adding another window to visualize total infected and healthy population.
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import csv
import pandas as pd

plt.style.use("dark_background")


# ------------------------------------------------------------
global day, s, x, y, day1, y1
# create a figure object and axes
fig = plt.figure(figsize=(14, 6))
gs1 = fig.add_gridspec(nrows=4, ncols=4)

# ax1 = fig.add_subplot(121, aspect='equal')
ax1 = fig.add_subplot((gs1[:, 0:3]), aspect="equal")
ax1.axis("off")
ax2 = fig.add_subplot(gs1[:2:3])

# ax2 = fig.add_subplot(122)
ax2.set_facecolor("gray")


# This helps in getting rid of margins on side of axes. Default is 5%
plt.rcParams["axes.xmargin"] = 0

# set bounds for the 'box'
bounds = [-100, 100, -100, 100]

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


n = 150
person = np.ones(
    n,
    dtype=[
        ("position", float, 2),
        ("velocity", float, 2),
        ("status", float, 1),
        ("duration", float, 1),
        ("size", float, 1),
        ("color", float, 4),
        ("facecolor", float, 4),
    ],
)


# initialize position, velocity, status, color and facecolor

person["position"] = np.random.uniform(-60, 60, size=(n, 2))
person["velocity"] = (-0.5 + np.random.random((n, 2))) * 80
person["color"] = np.zeros((n, 4))
person["color"][:, 1] = 0.5
person["color"][0] = [1.0, 0.0, 0.0, 1.0]
person["facecolor"] = np.zeros((n, 4))
person["facecolor"] = [0, 0.55, 0.52, 0.5]  # Set color to 'teal with alpha = 0.5

# initialize first infected person
person["facecolor"][0] = [1.0, 0.0, 0.0, 0.6]
person["position"][0] = [0.0, 0.0]
person["status"][0] = 0
person["duration"] = 0.0
# person['duration'][0] =


day = 0
day1 = 0.00
x = [0]
y = [0]
y1 = [100]
s = np.ones((n)) * 20
text1 = ax1.text(-10, 42, "")
text2 = ax1.text(-10, 100, "")

# create a scatter plot
with plt.style.context("dark_background"):
    scat = ax1.scatter(
        person["position"][:, 0],
        person["position"][:, 1],
        lw=0.5,
        s=s,
        label="day",
        edgecolors=person["color"],
        facecolors=person["facecolor"],
    )


data = pd.DataFrame(columns=["day", "infected", "recovered"])
data = data.fillna(0)

# Animation update function
def update(frame_number):

    current_index = frame_number % n

    global categories, rect, dt, ax, fig, colormap, legend, s, data

    day = int(frame_number / 20)

    day1 = frame_number / 20
    # print(day1)
    dt = 1 / 30  # 30fps
    infection_radius = 3.0
    social_distancing = 0.1

    # update location
    person["position"] += dt * person["velocity"]
    scat.set_offsets(person["position"])

    # check for crossing boundary

    crossed_x1 = person["position"][:, 0] < bounds[0] + person["size"] + 3
    crossed_x2 = person["position"][:, 0] > bounds[1] - person["size"] - 3
    crossed_y1 = person["position"][:, 1] < bounds[2] + person["size"] + 3
    crossed_y2 = person["position"][:, 1] > bounds[3] - person["size"] - 3

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
                person["facecolor"][i2] = [1, 0, 0, 0.6]

        elif person["status"][i2] == 0:
            person["status"][i1] = np.random.choice(
                [0, 1], p=[1 - social_distancing, social_distancing]
            )
            if person["status"][i1] == 0:
                person["color"][i1][0] = 1
                person["color"][i1][1] = 0
                person["facecolor"][i1] = [1, 0, 0, 0.6]

    active_infections = (person["status"] == 0).sum()
    infected_pcnt = int(active_infections / n * 100)
    recovered = (person["status"] == 2).sum()
    recovered_pcnt = int(recovered / n * 100)

    # update size of particles with status = 0
    s = np.where(person["status"] == 0, s + 8, s)
    s = np.where(s > 100, 20, s)
    s = np.where(person["status"] == 2, 20, s)

    # update infection duration of person
    person["duration"] = np.where(
        person["status"] == 0, person["duration"] + 0.05, person["duration"]
    )

    # Update status of person when infection duration > 15 days
    person["status"] = np.where(person["duration"] > 15, 2, person["status"])

    # update alpha value as function of size
    person["color"][:, 3] = np.where(person["status"] == 0, (1 - (s - 20) / 80), 1)

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

    # Update velocity of particles at the boundary
    person["velocity"][crossed_x1 | crossed_x2, 0] *= -1
    person["velocity"][crossed_y1 | crossed_y2, 1] *= -1

    # use set function to change color and sizes
    rect.set_edgecolor("w")

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
    ax2.set_ylim(ymin=0, top=100)
    ax2.set_xlim([0, day])
    ax2.autoscale(enable=True, axis="x", tight=None)
    ax2.plot(x, y, color="red", alpha=0.5)
    ax2.plot(x, y1, color="gray", alpha=0.5)
    ax2.fill_between(x, y, y2=0, color="red", alpha="0.5")
    ax2.fill_between(x, y1, y2=100, color="gray", alpha="0.5")
    ax2.fill_between(x, y, y1, color="teal", alpha="0.5")
    text2.set_position((200, 115))
    text2.set_text(
        f"Infected = {infected_pcnt}%   Removed/Recovered = {recovered_pcnt}%"
    )

    dict = {"day": day, "infected": infected_pcnt, "recovered": recovered_pcnt}
    data = data.append(dict, ignore_index=True)
    # if frame_number == 1100:
    #     data.to_csv('data.csv')

    return (scat,)


# Construct the animation, using the update function as the animation
# director.
animation = animation.FuncAnimation(fig, update, interval=10, frames=1100)
# save command below

# animation.save('im_2r.mp4', fps = 15.0, dpi=800 )

plt.show()
