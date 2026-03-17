# all of our functions
import numpy as np
from scipy.special import erf

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
            "effcy" : np.array([0.55, 0.55, 0.75, 0.82, 0.80, 0.05])
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

# Functions
def tau_dcmotor(omega, motor):
    
    # Validating if motor input is a valid dictionary  
    if not isinstance(motor, dict):
        raise Exception("Motor input must be a dictionary.")
    
    # Assigning each variable from motor dictionary
    torque_stall = motor["torque_stall"]
    torque_noload = motor["torque_noload"]
    speed_noload = motor["speed_noload"]
    
    # Testing if omega is scalar. Then calculating
    try:
        
        if omega < 0:
            return torque_stall
        elif omega > speed_noload:
            return  0
        else:
            return torque_stall - ((torque_stall - torque_noload) / 
                   speed_noload) * omega
    
    except Exception:
        pass # Omega is not scalar. Try next test.
    
    # Testing if omega is a numpy array. Then calculating.
    try:
    
        tau = np.zeros_like(omega,dtype = float) # Assinging 0s to tau (must be float)
    
        for i in range(len(tau)): # Individually goes through each number
        
            if omega[i] < 0:
                tau[i] = torque_stall
            elif omega[i] > speed_noload:
                tau[i] = 0
            else:
                tau[i] = torque_stall - ((torque_stall - torque_noload) / 
                   speed_noload) * omega[i]
    
        return tau

    except Exception:
        raise Exception("Omega input must be a scalar or an array")

###############################################################################
def get_gear_ratio(speed_reducer):
  # Validate inputs

  if not isinstance(speed_reducer, dict):
        raise Exception("Speed_reducer input needs to be a dictionary.")
  # Assigning each variable from speed_reducer dictionary
  type = speed_reducer["type"]
  diam_pinion = speed_reducer["diam_pinion"]
  diam_gear = speed_reducer["diam_gear"]
  mass = speed_reducer["mass"]
  # Math
  if type.lower() == "reverted":
      Ng = (diam_gear / diam_pinion)**2
  else:
      raise Exception("type needs to be reverted")

  return Ng
###############################################################################

def get_mass(rover):

    if not isinstance(rover, dict):
        raise Exception('Input is invalid: must be part of the dictionary')
#extract the sub parts of the dictionary
    
    wheel_assembly = rover['wheel_assembly']
    
    wheel = wheel_assembly['wheel']
    
    motor = wheel_assembly['motor']
    
    speed_reducer = wheel_assembly['speed_reducer']

    chassis = rover['chassis']
    
    science_payload = rover['science_payload']
    
    power_subsys = rover['power_subsys']

#list the mass of each object (kg)

    WheelMass = wheel['mass']

    MotorMass = motor['mass']

    SciencePayloadMass = science_payload['mass']

    RTGMass = power_subsys['mass']

    chassismass = chassis['mass']

    speed_reducermass = speed_reducer['mass']

    total_mass = WheelMass * 6 + MotorMass * 6 + speed_reducermass * 6 + SciencePayloadMass + RTGMass + chassismass
        
    return total_mass

##########################################################

def F_gravity(terrain_angle, rover, planet):
    
#account for potential errors 

    if np.any(terrain_angle > 75) or np.any(terrain_angle < -75):
        raise Exception('Angle input invalid: terrain angle must be between the angle of -75 and 75 degrees')
    
    if not isinstance(rover, dict):
        raise Exception('Rover input invalid: The input must be in the dictionary')
        
    if not isinstance(planet, dict):
        raise Exception('Planet input invalid: The input must be in the dictionary')
    
#List known values

    rover_mass = get_mass(rover)
    
    gravity = planet['g']

    angle = np.deg2rad(terrain_angle)
    
# calculate the force due to gravity

    gravitational_force = -rover_mass * gravity * np.sin(angle)

    return gravitational_force

############################################################################
def F_rolling(omega, terrain_angle, rover, planet, Crr):
    
#Account for poential errors

    if not isinstance(Crr, (int, float)) or Crr <= 0:
        raise Exception("Crr input invalid: must be a positive scalar")
    
    if np.any(terrain_angle > 75) or np.any(terrain_angle < -75):
        raise Exception('Angle input invalid: terrain angle must be between the angle of -75 and 75 degrees')
        
    if not isinstance(Crr, (int, float, np.ndarray)) or Crr <= 0:
        raise Exception('Crr input invalid: The input must be scalar and greater than 0')
        
    if not isinstance(rover, dict):
        raise Exception('Rover input invalid: The input must be in the dictionary')
        
    if not isinstance(planet, dict):
        raise Exception('Planet input invalid: The input must be in the dictionary')

    if omega.shape != terrain_angle.shape:
        raise Exception('Omega and terrain angle must be the same shape')
        
#List known values

    wm = rover['wheel_assembly']

    wheel = wm['wheel']
    
    rover_mass = get_mass(rover)

    sr = wm['speed_reducer']
    
    gravity = planet['g']
    
    gear_radius = wheel['radius']
    
    gear_ratio = get_gear_ratio(sr)
    
    angle = np.deg2rad(terrain_angle)

#calculate velocity of the rover

    rover_velocity = gear_radius * (omega / gear_ratio)
    
#calculate normal force

    Force_normal = rover_mass * gravity * np.cos(angle)
    
#calculate rolling resistance force

    Frolly =  -erf(40 * rover_velocity) * Crr * Force_normal

    return Frolly

############################################################################

def F_drive(omega, rover):
    # Validate scalor and dict
    if not np.isscalar(omega) and not isinstance(omega, np.ndarray):
            raise Exception("Omega input must be a scalar or an array.")
    if not isinstance(rover, dict):
            raise Exception("Speed_reducer input needs to be a dictionary.")
    

    wheel_assembly = rover['wheel_assembly']
    wheel = wheel_assembly['wheel']
    motor = wheel_assembly['motor']
    speed_reducer = wheel_assembly['speed_reducer']

    radius = wheel['radius']

    # Motor torque
    torque = tau_dcmotor(omega, motor)

    # Gear ratio
    Ng = get_gear_ratio(speed_reducer)
    # account for all 6 wheels
    Fd = 6 * (torque * Ng) / radius
    return Fd


################################################################

def F_net(omega, terrain_angle, rover, planet, Crr):

  
    #account for possible errors and raise exceptions for each one
   
    
    if np.any(terrain_angle > 75) or np.any(terrain_angle < -75):
        raise Exception('Angle input invalid: terrain angle must be between the angle of -75 and 75 degrees')

    if not np.isscalar(Crr) or Crr <= 0:
        raise Exception('Crr input invalid: The input must be a scalar and positive')
    
    #if not isinstance(Crr, (int, float)) or Crr <= 0:
        #raise Exception('Crr_1 input invalid: The input must be scalar and greater than 0')
        
    #if not isinstance(Crr, (int, float, np.ndarray)) or Crr <= 0:
       # raise Exception('Crr_1 input invalid: The input must be scalar and greater than 0')
        
    if not isinstance(rover, dict):
        raise Exception('Rover input invalid: The input must be in the dictionary')
        
    if not isinstance(planet, dict):
        raise Exception('Planet input invalid: The input must be in the dictionary')

    if np.size(omega) != np.size(terrain_angle) and np.size(omega) != 1 and np.size(terrain_angle) != 1:
        raise Exception('Omega and terrain angle must be the same shape')
    #calculate some of force 
    
    Force_net = F_gravity(terrain_angle, rover, planet) + F_rolling(omega, terrain_angle, rover, planet, Crr) + F_drive(omega, rover)
    
    return Force_net

"""###########################################################################
#   This file initializes the experiment and end_event structures for 
#   MEEN 357 project phase 2.
#
#   Created by: MEEN 357 Instructional Team
###########################################################################"""

import numpy as np

def experiment1():
    
    experiment = {'time_range' : np.array([0,20000]),
                  'initial_conditions' : np.array([0.325,0]),
                  'alpha_dist' : np.array([0, 100, 200, 300, 400, 500, 600, \
                                           700, 800, 900, 1000]),
                  'alpha_deg' : np.array([2.032, 11.509, 2.478, 7.182, \
                                        5.511, 10.981, 5.601, -0.184, \
                                        0.714, 4.151, 4.042]),
                  'Crr' : 0.1}
    
    
    # Below are default values for example only:
    end_event = {'max_distance' : 50,
                 'max_time' : 5000,
                 'min_velocity' : 0.01}
    
    return experiment, end_event

def end_of_mission_event(end_event):
    """
    Defines an event that terminates the mission simulation. Mission is over
    when rover reaches a certain distance, has moved for a maximum simulation 
    time or has reached a minimum velocity.            
    """
    
    mission_distance = end_event['max_distance']
    mission_max_time = end_event['max_time']
    mission_min_velocity = end_event['min_velocity']
    
    # Assume that y[1] is the distance traveled
    distance_left = lambda t,y: mission_distance - y[1]
    distance_left.terminal = True
    
    time_left = lambda t,y: mission_max_time - t
    time_left.terminal = True
    
    velocity_threshold = lambda t,y: y[0] - mission_min_velocity;
    velocity_threshold.terminal = True
    velocity_threshold.direction = -1
    
    # terminal indicates whether any of the conditions can lead to the
    # termination of the ODE solver. In this case all conditions can terminate
    # the simulation independently.
    
    # direction indicates whether the direction along which the different
    # conditions is reached matters or does not matter. In this case, only
    # the direction in which the velocity treshold is arrived at matters
    # (negative)
    
    events = [distance_left, time_left, velocity_threshold]
    
    return events

import numpy as np

def motorW(v, rover):
    
    """
    Compute motor angular speed from rover velocity.

    Inputs
    v : scalar or 1D numpy array
        Rover velocity [m/s]

    rover : dict
        Rover definition dictionary

    Returns
    w : scalar or numpy array
        Motor angular speed [rad/s]
    """
    
#raise exceptions in case of error input
    if not isinstance(rover, dict):
        raise Exception("Rover input is invalid")
    
    if not (np.isscalar(v) or isinstance(v, np.ndarray)):
        raise Exception("Velocity input is invalid, please input a scalar or numpy array")
        
    if isinstance(v, np.ndarray) and v.ndim > 1:
        raise Exception("Velocity input is invalid because it is not 1-Dimensional")
    
    wm = rover['wheel_assembly']

    wheel = wm['wheel']
    
    radius = wheel["radius"]
    

    gear_ratio = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    
    v = np.array(v)
    
    w_wheel = v / radius
    
    angular_speed = gear_ratio * w_wheel
    
    return angular_speed

def rover_dynamics(t, y, rover, planet, experiment):
    
    """
    This function computes the derivative of the state vector (state vector is: [velocity, position]) for the rover given its
    current state. It requires rover and experiment dictionary input parameters. It is intended to be passed to an ODE
    solver.
    
    Input: 
        t scalar Time sample [s]
        
        y 1D numpy array Two-element array of dependent variables (i.e., state vector). First
        element is rover velocity [m/s] and second element is rover position [m]
        
        rover dict Data structure containing rover definition
        
        planet dict Data structure containing planet definition
        
        experiment dict Data structure containing experiment definition
    
    Output:
        
        dydt 1D numpy array Two-element array of first derivatives of state vector. First element is
        rover acceleration [m/s^2] and second element is rover velocity [m/s]
    
    """

    from scipy.interpolate import interp1d
    
#raise exceptions in case of error
    if not isinstance(rover, dict):
        raise Exception("Rover input is invalid")
        
    if not isinstance(planet, dict):
         raise Exception("Planet input is invalid")
         
    if not isinstance(y, np.ndarray):
         raise Exception("y input is invalid")
        
    if not isinstance(experiment, dict):
        raise Exception("experiment input is invalid")
    if y.size != 2:
        raise Exception("y size should be equal to 2")

#Extract necessary variables

    velocity = y[0]
    
    position = y[1]
    
    alpha_dist = experiment['alpha_dist']
    
    alpha_deg = experiment['alpha_deg']
    
    Crr = experiment['Crr']
    
    omega = motorW(velocity, rover)
#interpolate terrain angle

    terrain = interp1d(alpha_dist, alpha_deg, kind = 'cubic', fill_value = "extrapolate")
    terrain_angle = terrain(position)
    
# Force calculations

    Force_drive = F_drive(omega,rover)
    
    Force_rolling = F_rolling(omega, terrain_angle, rover, planet, Crr)
    
    Force_gravity = F_gravity(terrain_angle, rover, planet)
    
    Force_net = Force_drive + Force_rolling + Force_gravity
    
#caclulate acceleration

    mass = get_mass(rover)
    
    acceleration = Force_net / mass
    

#Find first derivative dydt

    dydt = np.array([acceleration, velocity])
    return dydt
    
    
    
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
    tau = tau_dcmotor(angular_speed, rover['wheel_assembly']['motor'])
    
#Calculate motor power

    Power = tau * angular_speed
    
    return Power


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

def simulate_rover(rover, planet, experiment, end_event):
    
    """
    This function integrates the trajectory of a rover to find the time,
    velocity, and position of the rover. All of this is then added to
    the rover dictionary, along with other parameters found during this 
    part of the project.
    
    Input Arguments:
        rover = dictionary containing the parameters of the rover
        planet = dictionary of the planet definition
        experiment = dictionary containing the parameters of the trajectory
        end_event = dictionary containing when to terminate simulation
    
    Returns:
        rover = an updated dictionary including telemetry information
    """
    
    # Imports
    import numpy as np
    from scipy.integrate import solve_ivp
    
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
    experiment, end_event = experiment1() # importing 
    
    y0 = experiment["initial_conditions"]
    time_range = experiment["time_range"]
    
    # Event function to solve future ODE 
    terminate = end_of_mission_event(end_event)
    
    # Rover dynamics function (must be used in solve_ivp)
    def r_dynamics(t, y):
        return rover_dynamics(t, y, rover, planet, experiment)
    
    # Solving the ODE which will givea list of time, velocity, and position
    trajectory = solve_ivp(r_dynamics, time_range, y0, events = terminate, max_step = 1)
    
    # Results where trajectory is represented in time values and gives y
    time = trajectory.t
    velocity = trajectory.y[0]
    position = trajectory.y[1]
    
    # Collecting data needed to add to rover dictionary
    
    completion_time = time[-1] # Total time should be the final time 
    distance_traveled = position[-1] # Gives final position
    max_velocity = np.max(velocity)
    average_velocity = np.average(velocity)
    
    # Importing power and battery energy from previous functions
    power = 6 * mechpower(v, rover)
    battery_energy = battenergy(t, v, rover)
    energy_per_distance = battery_energy / distance_traveled
    
    # Adding telemetry to rover\
    rover["telemetry"] = {
        "Time": time,
        "completion_time": completion_time,
        "velocity": velocity,
        "position": position,
        "distance_traveled": distance_traveled,
        "max_velocity": max_velocity,
        "average_velocity": average_velocity,
        "power": power,
        "battery_energy": battery_energy,
        "energy_per_distance": energy_per_distance
        }
    
    return rover
    
