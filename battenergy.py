# Function
def battenergy(t, v, rover):
    
    """ This function computes the total electrical energy consumed from 
    the rover battery pack. It is assumed that all 6 motors are used at
    the same time for simplification.
    
    Inputs should be the following:
        t = 1D numpy arrau of time samples from a rover simulation [s]
        v = 1D numpy arrau of rover velocity data from a simulation [m/s]
        rover = dictionary
    """
    
    # Imports
    import numpy as np
    from scipy.interpolate import interp1d
    
    # Checking the validity of inputs
    if not isinstance(t, np.ndarray) or not isinstance(v, np.ndarray):
        raise Exception("t and v inputs must be numpy arrays")
    if len(t) != len(v):
        raise Exception("t and v should be equal length vectors")
    if not isinstance(rover, dict):
        raise Exception("rover should be a dictionary")
    
    # Get motor information from rover dictionary
    motor = rover['wheel_assembly']['motor']
    
    # Plug into functions to get power
    mech_power = mechpower(v, rover)
    
    
    # Calling motorW to get angular speed and then calculating tau
    omega = motorW(v, rover)
    tau = tau_dcmotor(omega, motor)
    
    # Efficiency as a function of torque
    tau_efficiency = rover['wheel_assembly']['motor']['effcy_tau']
    efficiency = rover['wheel_assembly']['motor']['effcy']
    
    # Interpolate values 
    final_efficiency_function = interp1d(tau_efficiency, efficiency, kind = "cubic", fill_value = "extrapolate")
    final_efficiency = final_efficiency_function(tau)
    
    # Calculating Power
    elect_power = mech_power / final_efficiency
    # power = 6 * elect_power
    
    # Integrating using trapezoidal method to get electrical energy consumed
    E = 6 * np.trapz(elect_power, t)
    
    return E
