
from subfunctions import *


# Function
def battenergy(t, v, rover):
    
    # Imports
    import numpy as np
    
    
    # Checking the validity of inputs
    if len(t) != len(v):
        raise Exception("t and v should be equal length vectors")
    if isinstance(rover, dict):
        raise Exception("rover should be a dictionary")
    
    # Calling motorW to get angular speed
    omega = motorW(v, rover)
    
    # Get motor information from rover dictionary
    motor = rover['wheel_assembly']['motor']
    
    # Plug into functions to get tau and power
    tau = tau_dcmotor(omega, motor)
    mech_power = mechpower(v, rover)
    
    # Efficiency as a function of torque
    tau_efficiency = 
    efficiency = 
    
    # Interpolate values 
    eff_interpolate = interp1d(tau_efficiency, efficiency, fill_value = 'extrapolate')
    final_efficiency = eff_interpolate(tau)
    
    # Calculating Power
    power = 6 * mech_power / final_efficiency
    
    # Integrating using trapezoidal method to get electrical energy consumed
    E = np.trapz(power, t)
    
    return E