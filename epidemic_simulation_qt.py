"""
Epidemic/Pandemic spread simulation (no visualization). CAUTION: Simulation below can run for hours depending on on list 
r_l an q_l
"""
import numpy as np
import matplotlib.animation as animation
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import math
import pandas as pd


data = pd.DataFrame(
    columns=[
        "sim",
        "day",
        "infected",
        "recovered",
        "quarantined",
        "total_infections",
        "q",
        "ir",
        "sd",
    ]
)
data = data.fillna(0)
r_l = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
q_l = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
z_max = 2000
for r in r_l:

    for q in q_l:
        for sim in range(10):
            # ------------------------------------------------------------
            global day, s, x, y, day1, y1
            day = 0
            day1 = 0

            # Global Quarantine Flag: 0 for off, 1 for on
            quarantine = 1

            # quarantine probability
            q = q

            # Infection radius:
            infection_radius = r

            # Social distancing factor: 0- no social distancing, 1: complete distancing
            social_distancing = 0.0

            # set bounds for the 'box'
            bounds = [-100, 100, -100, 100]
            bounds3 = [-20, 20, -150, -110]

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

            #####
            # Global Quarantine Flag##
            # 0 for off, 1 for on
            quarantine = 1

            # initialize position, velocity, status, color and facecolor

            person["position"] = np.random.uniform(-40, 40, size=(n, 2))
            person["velocity"] = (-0.5 + np.random.random((n, 2))) * 50
            person["color"] = np.zeros((n, 4))
            person["color"][:, 1] = 0.5
            person["color"][0] = [1.0, 0.0, 0.0, 1.0]
            person["facecolor"] = np.zeros((n, 4))
            person["facecolor"] = [
                0,
                0.55,
                0.52,
                1.0,
            ]  # Set color to 'teal with alpha = 1.0

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
            s = np.ones((n)) * 20
            # text1 = ax1.text(-10, 42, "")
            # text2 = ax1.text(-10, 100, "")
            # text3 = ax1.text(-10, 42, "")

            # # create a scatter plot
            # scat = ax1.scatter(
            #     person["position"][:, 0],
            #     person["position"][:, 1],
            #     lw=0.5,
            #     s=s,
            #     label="day",
            #     edgecolors=person["color"],
            #     facecolors=person["facecolor"],
            # )

            # (line1,) = ax2.plot(x, y)
            # (line2,) = ax2.plot(x, y1)

            # Animation update function
            for z in range(z_max):
                frame_number = z
                day = int(frame_number / 20)
                day1 = frame_number / 20
                # print(day1)
                dt = 1 / 30  # 30fps

                # update location

                for i in range(n):
                    if (person["qtflag"][i] != 2) and person["position"][i][1] > -100:
                        person["position"][i][0] += dt * person["velocity"][i][0]
                        person["position"][i][1] += dt * person["velocity"][i][1]

                # scat.set_offsets(person["position"])

                crossed_x1 = (
                    person["position"][:, 0] < bounds[0] + person["size"] + 3
                ) & (person["qtflag"] != 2)
                crossed_x2 = (
                    person["position"][:, 0] > bounds[1] - person["size"] - 3
                ) & (person["qtflag"] != 2)
                crossed_y1 = (
                    person["position"][:, 1] < bounds[2] + person["size"] + 3
                ) & (person["qtflag"] != 2)
                crossed_y2 = (
                    person["position"][:, 1] > bounds[3] - person["size"] - 3
                ) & (person["qtflag"] != 2)

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
                                [0, 1], p=[0.1, 0.9]
                            )  # quarantine flag

                # Used to turn on/off quarantine
                if quarantine == 0:
                    person["qtflag"] = 0

                total_infections_pct = int(
                    (((person["status"] == 0) + (person["status"] == 2)).sum())
                    / n
                    * 100
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
                s = np.where(person["status"] == 0, s + 8, s)
                s = np.where(s > 100, 20, s)
                s = np.where(person["status"] == 2, 20, s)
                s = np.where(person["qtflag"] == 1, 20, s)

                # Update status of person when infection duration > 21 days
                person["status"] = np.where(
                    person["duration"] > 21, 2, person["status"]
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
                person["color"][:, 3] = np.where(
                    person["status"] == 0, (1 - (s - 20) / 80), 1
                )

                # changing edgecolor of persons with status =2 (recovered/removed)
                person["color"][:, 2] = np.where(
                    person["status"] == 2, 0.5, person["color"][:, 2]
                )
                person["color"][:, 1] = np.where(
                    person["status"] == 2, 0.5, person["color"][:, 1]
                )
                person["color"][:, 0] = np.where(
                    person["status"] == 2, 0.5, person["color"][:, 0]
                )

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

                dict = {
                    "sim": sim,
                    "day": day,
                    "infected": infected_pcnt,
                    "quarantined": quarantined,
                    "recovered": recovered_pcnt,
                    "total_infections": total_infections_pct,
                    "q": q,
                    "ir": infection_radius,
                    "sd": social_distancing,
                }
                data = data.append(dict, ignore_index=True)
                print(
                    f"sim = {sim}, q = {q}, ir = {r}, Day = {day} , Active infections = {active_infections}, Total Infections = {total_infections_pct}"
                )
                if z == z_max - 1:
                    data.to_csv("dataq.csv")
                z = z + 1
            active_infections = 0
            recovered = 0
            quarantined = 0
            total_infections_pct = 0
            sim = sim + 1
