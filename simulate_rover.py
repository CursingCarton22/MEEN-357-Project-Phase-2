
# Imports
from subfunctions import *
import numpy as np


def simulate_rover(rover,planet,experiment,end_event):
    
    # Checking the validity of inputs 
    if not isinstance(rover, dict):
        raise Exception("rover must only be a dictionary")
    if not isinstance(planet, dict):
        raise Exception("planet must only be a dictionary")
    if not isinstance(experiment, dict):
        raise Exception("experiment must only be a dictionary")
    if not isinstance(end_event, dict):
        raise Exception("end_event must only be a dictionary")
    
    # Initial conditions in experiment1
    initial = experiment("initial_conditions")
    time_range = experiment("time_range")
    
    

