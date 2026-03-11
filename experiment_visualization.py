
# Imports

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from subfunctions import *

# Variables

experiment, end_event = experiment1()

alpha_dist = experiment['alpha_dist']
alpha_deg = experiment['alpha_deg']

# Creating 100 data points
data_points = np.linspace(alpha_dist[0], alpha_dist[-1], num = 100)

# Code given in project to interpolate for terrain angles between data points
alpha_fun = (interp1d(alpha_dist, alpha_deg, kind = 'cubic', 
                      fill_value= 'extrapolate')) # fit the cubic spline

# Finding the angles at each point
angle_points = alpha_fun(data_points)

# Plotting Graphs
plt.figure()
plt.plot(alpha_dist, alpha_deg, marker = "*")
plt.plot(data_points, angle_points)
plt.xlabel('Position (m)')
plt.ylabel('Terrain Angle (deg)')

plt.title("Visualizing the Terrain")
