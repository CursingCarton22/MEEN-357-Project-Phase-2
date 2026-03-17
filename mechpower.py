# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 23:33:17 2026

@author: haide
"""
import numpy as np

def mechpower(v, rover):
    
    """
    Computes the instantaneous
    mechanical power output by a single DC motor at each point 
    in a simulation run, in Watts.
    
    Input:
        
    v - rover velocity [v/s]
    
    rover - rover data structure dictionary
    
    Return:
        
    Power - Mechanical Power Output [W]

    """
#raise exceptions in case of error
    
    if not isinstance(rover, dict):
        raise Exception("Rover input is invalid")
    
    if not (np.isscalar(v) or isinstance(v, np.ndarray)):
        raise Exception("Velocity input is invalid, please input a scalar or numpy array")
        
    if isinstance(v, np.ndarray) and v.ndim > 1:
        raise Exception("Velocity input is invalid because it is not 1-Dimensional")
        
#calculate motor speed

    angular_speed = motorW(v, rover)
    
#calculate motor torque
    torque = tau_dcmotor(w, rover)
    
#Calculate motor power

    Power = torque * angular_speed
    
    return Power
    
    
        
    
