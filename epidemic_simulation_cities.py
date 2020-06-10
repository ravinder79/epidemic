"""
Epidemic/Pandemic spread simulation. Simulation only, no visulization
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math
import hop
import pandas as pd


# ------------------------------------------------------------
global day, s, x, y, day1, y1
day = 0
day1 = 0
t = 0


##### Settings###
# Global Quarantine Flag: 0 for off, 1 for on
quarantine = 1

# quarantine probability
q = 0.9

# Infection radius:
infection_radius = 0.8

# Social distancing factor: 0- no social distancing, 1: complete distancing
social_distancing = 0.0


# set bounds for the 'box'
bounds = [-100, 100, -100, 100]
bounds_1 = [-100, -40, -100, -40]
bounds_2 = [-30, 30, -100, -40]
bounds_3 = [40, 100, -100, -40]

bounds_4 = [-100, -40, -30, 30]
bounds_5 = [-30, 30, -30, 30]
bounds_6 = [40, 100, -30, 30]

bounds_7 = [-100, -40, 40, 100]
bounds_8 = [-30, 30, 40, 100]
bounds_9 = [40, 100, 40, 100]
# bounds = [-100, 100, -100, 100]
boundaries = pd.concat(
    [
        pd.DataFrame(bounds_1),
        pd.DataFrame(bounds_2),
        pd.DataFrame(bounds_3),
        pd.DataFrame(bounds_4),
        pd.DataFrame(bounds_5),
        pd.DataFrame(bounds_6),
        pd.DataFrame(bounds_7),
        pd.DataFrame(bounds_8),
        pd.DataFrame(bounds_9),
        pd.DataFrame(bounds),
    ],
    axis=1,
)
boundaries.columns = [
    "bounds_1",
    "bounds_2",
    "bounds_3",
    "bounds_4",
    "bounds_5",
    "bounds_6",
    "bounds_7",
    "bounds_8",
    "bounds_9",
    "bounds",
]

center = pd.DataFrame(
    [
        [-70, -70],
        [0, -70],
        [70, -70],
        [-70, 0],
        [0, 0],
        [70, 0],
        [-70, 70],
        [0, 70],
        [70, 70],
    ]
)
center.columns = ["x", "y"]


# central location bounds
cbounds = [-4, 4, -4, 4]

# Quarantine boundaries
bounds3 = [-20, 20, -150, -110]


for i in range(9):
    n = 500
    person = np.ones(
        n,
        dtype=[
            ("position", float, 2),
            ("velocity", float, 2),
            ("trip", int, 1),
            ("status", int, 1),
            ("counter", int, 1),
            ("qtflag", int, 1),
            ("box", int, 1),
            ("duration", float, 1),
            ("size", float, 1),
            ("color", float, 4),
            ("facecolor", float, 4),
        ],
    )

for i in range(n):
    person["box"][i] = np.random.choice([1, 2, 3, 4, 6, 7, 8, 9])

for j in range(0, n):
    b = person["box"][j]
    offset = 5
    person["position"][j][0] = np.random.uniform(
        (boundaries.iloc[0, b - 1] + offset),
        (boundaries.iloc[1, b - 1] - offset),
        size=(1, 1),
    )[0][0]
    person["position"][j][1] = np.random.uniform(
        (boundaries.iloc[2, b - 1] + offset),
        (boundaries.iloc[3, b - 1] - offset),
        size=(1, 1),
    )[0][0]

# Status definitions:
# 0: Infected
# 1: suseptible
# 2: Recovered/Removed


# initialize position, velocity, status, color and facecolor

person["velocity"] = (-0.5 + np.random.random((n, 2))) * 80
person["color"] = np.zeros((n, 4))
person["color"][:, 1] = 0.5
person["color"][0] = [1.0, 0.0, 0.0, 1.0]
person["facecolor"] = np.zeros((n, 4))
person["facecolor"] = [0, 0.55, 0.52, 1.0]  # Set color to 'teal with alpha = 1.0

# initialize first infected person
person["facecolor"][0] = [1.0, 0.0, 0.0, 0.6]
# person['position'][0] = [-80.0 , -80.0]
person["status"][0] = 0

person["duration"] = 0.0
person["qtflag"] = 0
person["trip"] = 0
person["counter"] = 0

t1 = 0
day = 0
day1 = 0.00
x = [0]
y = [0]
y1 = [100]
s = np.ones((n)) * 3

data = pd.DataFrame(columns=["sim", "day", "infected", "recovered", 'quarantined','total_infections', 'q', 'ir', 'sd'])
data = data.fillna(0)
z_max = 2000
#####################################################################################################
for sim in range(10):
    for z in range(z_max):
        frame_number = z

        global  dt, ax, colormap, legend

        day = int(frame_number / 20)
        day1 = frame_number / 20
        dt = 1 / 30  # 30fps
        

        # update location

        for i in range(n):
            if (
                (person["qtflag"][i] != 2)
                and (person["position"][i][1] > -110)
                and (person["trip"][i] == 0)
            ):
                person["position"][i][0] += dt * person["velocity"][i][0]
                person["position"][i][1] += dt * person["velocity"][i][1]

        # scat.set_offsets(person["position"])

        # Check if any person crossed the boundary
        crossed_x = []
        crossed_y = []

        for i in range(0, n):
            if person["trip"][i] == 0:
                b = person["box"][i]
                crossed_x1 = (
                    person["position"][i][0]
                    < boundaries.iloc[0, b - 1] + person[i]["size"] + 1
                ) & (person[i]["qtflag"] != 2)
                crossed_x2 = (
                    person["position"][i][0]
                    > boundaries.iloc[1, b - 1] - person[i]["size"] - 1
                ) & (person[i]["qtflag"] != 2)
                crossed_y1 = (
                    person["position"][i][1]
                    < boundaries.iloc[2, b - 1] + person[i]["size"] + 1
                ) & (person[i]["qtflag"] != 2)
                crossed_y2 = (
                    person["position"][i][1]
                    > boundaries.iloc[3, b - 1] - person[i]["size"] - 1
                ) & (person[i]["qtflag"] != 2)

                crossed_x.append(crossed_x1 | crossed_x2)
                crossed_y.append(crossed_y2 | crossed_y1)

            if person["trip"][i] == 1:

                crossed_x1 = (
                    person["position"][i][0] < boundaries.iloc[0, 9] + person[i]["size"] + 1
                ) & (person[i]["qtflag"] != 2)
                crossed_x2 = (
                    person["position"][i][0] > boundaries.iloc[1, 9] - person[i]["size"] - 1
                ) & (person[i]["qtflag"] != 2)
                crossed_y1 = (
                    person["position"][i][1] < boundaries.iloc[2, 9] + person[i]["size"] + 1
                ) & (person[i]["qtflag"] != 2)
                crossed_y2 = (
                    person["position"][i][1] > boundaries.iloc[3, 9] - person[i]["size"] - 1
                ) & (person[i]["qtflag"] != 2)

                crossed_x.append(crossed_x1 | crossed_x2)
                crossed_y.append(crossed_y2 | crossed_y1)

        # Update velocity of persons which crossed boundries
        person["velocity"][crossed_x, 0] *= -1
        person["velocity"][crossed_y, 1] *= -1

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
            ) or ((person["qtflag"][i2] == 2) or (person["qtflag"][i1] == 2)):
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
                        [0, 1], p=[1 - q, q]
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

        total_infections_pct = int(
            (((person["status"] == 0) + (person["status"] == 2)).sum()) / n * 100
        )
        active_infections = (person["status"] == 0).sum()
        infected_pcnt = int(active_infections / n * 100)
        recovered = (person["status"] == 2).sum()
        recovered_pcnt = int(recovered / n * 100)
        quarantined = (person["qtflag"] == 2).sum()

        # update infection duration of person
        person["duration"] = np.where(
            person["status"] == 0, person["duration"] + 0.05, person["duration"]
        )

        # The section below is for people going back and forth to a central location###
        t1 = (person["trip"] == 1).sum()
        t0 = np.where((person["trip"] == 0))[0]

        if t1 == 0:
            cl = np.random.choice(t0, size=12)
            for c in cl:
                person["trip"][c] = 1
            po = person["position"][cl]

        t1 = (person["trip"] == 1).sum()

        if t1 < 12:
            xs = np.where(person["trip"][cl] == 0)[0]
            for i in xs:
                list1 = np.where(person["trip"] == 0)[0]
                cl[i] = np.random.choice(list1, 1)

            for c in cl:
                person["trip"][c] = 1

        # hopping to central location
        po = [0, 0]
        for c in cl:

            po[0] = center.iloc[10 - person["box"][c] - 1, 0]
            po[1] = center.iloc[10 - person["box"][c] - 1, 1]

            if person["trip"][c] == 1 and person["counter"][c] <= 5:
               
                person["position"][c][0], person["position"][c][1] = hop.linehop(
                    0, 0, person["position"][c][0], person["position"][c][1]
                )

            if (abs(person["position"][c][0]) < 5) and (abs(person["position"][c][1]) <= 5):
                person["counter"][c] = person["counter"][c] + 1

            if person["box"][c] % 2 != 0:
                if person["counter"][c] > 8 and (
                    (abs(person["position"][c][0]) < abs(po[0]))
                    or (abs(person["position"][c][1]) < abs(po[1]))
                ):
                    person["position"][c][0] = hop.hopr(po[0], person["position"][c][0])
                    person["position"][c][1] = hop.hopr(po[1], person["position"][c][1])

                if (person["counter"][c] > 8) and (
                    (abs(person["position"][c][0]) - abs(po[0]) >= 0)
                    or (abs(person["position"][c][1]) - abs(po[1]) >= 0)
                ):
                    person["trip"][c] = 0
                    person["counter"][c] = 0
                    person["box"][c] = 10 - person["box"][c]

            if (person["box"][c] == 2) or (person["box"][c] == 8):
             
                if (person["counter"][c]) > 8 and (
                    abs(person["position"][c][1]) < abs(po[1])
                ):
                    person["position"][c][1] = hop.hopr(po[1], person["position"][c][1])

                if (person["counter"][c] > 8) and (
                    abs(person["position"][c][1]) - abs(po[1]) >= 0
                ):
                    person["trip"][c] = 0
                    person["counter"][c] = 0
                    person["box"][c] = 10 - person["box"][c]

            if (person["box"][c] == 4) or (person["box"][c] == 6):

                if person["counter"][c] > 8 and (
                    abs(person["position"][c][0]) < abs(po[0])
                ):
                    person["position"][c][0] = hop.hopr(po[0], person["position"][c][0])

                if (person["counter"][c] > 8) and (
                    abs(person["position"][c][0]) - abs(po[0]) >= 0
                ):
                    person["trip"][c] = 0
                    person["counter"][c] = 0
                    person["box"][c] = 10 - person["box"][c]

        # End of central location visit code block#

        # quarantine code.
        stepx = 15
        stepy = 15
        for i in range(
            len(
                (person["qtflag"] == 1)
                & (person["position"][:, 1] >= -100)
                & (person["duration"] > 1)
                & (person["trip"] == 0)
            )
        ):

            if (
                (person["qtflag"][i] == 1)
                & (person["position"][i][1] >= -100)
                & (infected_pcnt + recovered_pcnt > 10)
                & (person["duration"][i] > 1)
                & (person["trip"][i] == 0)
                & (
                    (person["box"] == person["box"][i]).sum()
                    - person["status"][person["box"] == person["box"][i]].sum()
                    > 5
                )
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

        # Update status of person when infection duration > 15 days
        person["status"] = np.where(person["duration"] > 15, 2, person["status"])

        # return of quarantined persons who have recovered after 21 days
        lsq = np.where((person["qtflag"] == 2) & (person["status"] == 2))
        lsq = lsq[0]

        for i in lsq:
            po[0] = center.iloc[person["box"][i] - 1, 0]
            po[1] = center.iloc[person["box"][i] - 1, 1]
            person["position"][i][1] = po[1]
            person["position"][i][0] = po[0]
            person["qtflag"][i] = 0

        #### End quarantine code block###

        #### Appending data to a  dict and saving as csv
        dict = {"sim" : sim, "day": day, "infected": infected_pcnt, "quarantined": quarantined, "recovered": recovered_pcnt, 'total_infections' : total_infections_pct, 'q': q, 'ir': infection_radius, 'sd':social_distancing}
        data = data.append(dict, ignore_index=True)
        print(f'sim = {sim}, z = {z}, Day = {day} , Active infections = {active_infections}, Total Infections = {total_infections_pct}')
        if z == z_max:
            data.to_csv('data.csv')
        z = z+1
    sim = sim + 1
    