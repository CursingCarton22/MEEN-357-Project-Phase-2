# Imports

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from subfunctions import *

# Variables

experiment, end_event = experiment1()

alpha_dist = experiment['alpha_dist']
alpha_deg = experiment['alpha_deg']

# Creating 100 data points and finding the range by using the first and last distances
data_points = np.linspace(alpha_dist[0], alpha_dist[-1], num = 100)

# Code given in project to interpolate for terrain angles between data points
alpha_fun = (interp1d(alpha_dist, alpha_deg, kind = 'cubic', 
                      fill_value= 'extrapolate')) # fit the cubic spline

# Finding the angles at each point by plugging data_points into alpha_fun
angle_points = alpha_fun(data_points)

# Plotting Graphs
plt.figure()
plt.plot(alpha_dist, alpha_deg, marker = "*") # Plot of the known values
plt.plot(data_points, angle_points) # Plot of the interpolated values
plt.xlabel('Position (m)')
plt.ylabel('Terrain Angle (deg)')
plt.title("Visualizing the Terrain")
