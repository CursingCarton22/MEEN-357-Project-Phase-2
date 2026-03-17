# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 18:06:25 2026

@author: haide
"""

import numpy as np

import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
#copy and pasted dictionary from previous project phase. Added effcy_tau and effcy to it.
rover = {
    "wheel_assembly" : {
        "wheel" : {
            "radius" : 0.3,
            "mass" : 1
            },
        "speed_reducer" : {
            "type" : "reverted",
            "diam_pinion" : 0.04,
            "diam_gear" : 0.07,
            "mass" : 1.5
            },
        "motor" : {
            "torque_stall" : 170,
            "torque_noload" : 0,
            "speed_noload" : 3.8,
            "mass" : 5,
            "effcy_tau" : np.array([0, 10, 20, 40, 75, 165]),
            "effcy" : np.array([0, 0.55, 0.75, 0.82, 0.80, 0.05])
            }
        },
    "chassis" : {
        "mass" : 659
        },
    "science_payload" : {
        "mass" : 75
        },
    "power_subsys" : {
        "mass" : 90
        } 
    }

planet = {
    "g" : 3.72
    }

#dividing effct_tau by 100 to convert mm to m
efficiency_tau = rover["wheel_assembly"]["motor"]["effcy_tau"] 

#multiplying effcy by 100 to convert decimal to percentage point

efficiency = rover["wheel_assembly"]["motor"]["effcy"] * 100

#using PchipInterp. to make function

function = interp1d(efficiency_tau, efficiency, kind = 'cubic')

#making tau values

tau_values = np.linspace(min(efficiency_tau), max(efficiency_tau), 100)

#finding efficiency values

efficiency_values = function(tau_values)

#plotting the code on a graph

plt.figure()

plt.plot(tau_values, efficiency_values, label="Efficiency curve")

#graph doesnt look exactly like the graph on the manual. Asked people on stackoverflow for advice, they were condescending assholes and didnt answer my questions

plt.xlabel("Motor Torque [N-m]")
plt.ylabel("Efficiency [%]")
plt.title("Motor Efficiency vs Torque")
plt.legend()
plt.grid(True)

plt.show()
