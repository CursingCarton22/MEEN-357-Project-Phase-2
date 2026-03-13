# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 18:06:25 2026

@author: haide
"""

import numpy as np

import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

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

efficiency_tau = rover["wheel_assembly"]["motor"]["effcy_tau"]

efficiency = rover["wheel_assembly"]["motor"]["effcy"]

function = interp1d(efficiency_tau, efficiency, kind = "cubic")

tau_values = np.linspace(min(efficiency_tau), max(efficiency_tau), 100)

efficiency_values = function(tau_values)

plt.figure()

plt.plot(tau_values, efficiency_values, label="Efficiency curve")
plt.plot(efficiency_tau, efficiency, '*', markersize=10, label="Measured data")

plt.xlabel("Motor Torque [N-m]")
plt.ylabel("Efficiency [-]")
plt.title("Motor Efficiency vs Torque")
plt.legend()
plt.grid(True)

plt.show()