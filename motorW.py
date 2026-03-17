# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 00:07:02 2026

@author: haide
"""

import numpy as np

def motorW(v, rover):
    
    """
    This code computer the rotational speed (angular velocity) of the motor 
    depending on the translational velocity of the rover
    
    Input:
        
    v - rover velocity [m/s]
    
    rover - dictionary containing necessary values
    
    Results:
        
    angular_speed - Returns the motor speed/angular speed[rad/s]
    """
#raise exceptions in case of error input
    if not isinstance(rover, dict):
        raise Exception("Rover input is invalid")
    
    if not (np.isscalar(v) or isinstance(v, np.ndarray)):
        raise Exception("Velocity input is invalid, please input a scalar or numpy array")
        
    if isinstance(v, np.ndarray) and v.ndim > 1:
        raise Exception("Velocity input is invalid because it is not 1-Dimensional")

    #stating necessary values
    
    wm = rover['wheel_assembly']

    wheel = wm['wheel']
    
    radius = wheel["radius"]

    #using get_gear_ratio function to get gear_ratio
    
    gear_ratio = get_gear_ratio(rover)

    #calculating angular frequency
    
    w_wheel = v / radius

    #calculating angular speed
    
    angular_speed = gear_ratio * w_wheel
    
    return angular_speed
    
    
    
    
    
    
