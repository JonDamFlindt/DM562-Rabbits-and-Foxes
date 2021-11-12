import parameters
import simulation as sim
import reporting as report
from typing import List, Union

# Setting up menus
start_menu = ['display parameters', 'quick setup', 'advanced setup', 'run', 'quit']
advanced_menu = ['world', 'rabbits', 'foxes', 'execution', 'done']
reporting_menu = ['print summary', 'plot pop. size / time', 'plot lifespan', 'plot energy', 'plot kills distrubution', 'quit']

# Setting up variable changers
quick_vars = ['north/south length', 'west/east length', 'initial rabbits', 'initial foxes', 'max steps', 'batch (no visuals)']
quick_types = [int] * 5 + [bool]

adv_world = ['shape', 'north/south length', 'west/east length']
adv_pop = ['initial size', 'max age', 'max energy', 'metabolism', 'reproduction probability', 'min reproduction age', 'min reproduction energy']
adv_exe = ['max steps', 'batch (no visuals)']
adv_world_types = [str, int, int]
adv_pop_types = [int] * 4 + [float, int, int]
adv_exe_types = [int, bool]


quick_param_msg = """QUICK PARAMETERS:
world: {} by {} (n/s by w/e)
initial rabbits: {}
initial foxes: {}
max steps: {}
mode: {}"""


params = parameters.Simulation()



def _user_input(*msg: str):
  """Awaits an input and removes any excess spaces"""
  user = input(' '.join(msg) + ': ').lower() #User input, removes capitalization
  user = ' '.join([word for word in user.split(' ') if word != '']) # Handles any extra spaces in input
  return user

def is_integer(number: str) -> bool: #Shares name with the float method
  """Returns whether or not the given string is an integer."""
  return number.replace('.', '', 1).isdecimal() and float(number).is_integer()

def menu(menu_list: List[str]) -> str:
  """Menu function:
  Prints a list of options which the user can choose as input given a list.
  User input is either a number (e.g. "1." or "1") or a string (e.g. "Done")
  """

  state = None # Initialize variable
  viable_states = range(len(menu_list)) #Get viable states from the menu

  while True:
    print("\nAction selection:")
    for option in viable_states: #Prints all menu options
      print(str(option + 1) + '.', menu_list[option].capitalize())

    state = _user_input("Awaiting input")
    print()

    if is_integer(state) and float(state) - 1 in viable_states: #Handles floats/dots
        return menu_list[int(float(state)) - 1]
  
    elif state in menu_list:
      return state
    input("Invalid input, please try again (hit enter).") # Only printed if invalid state


def input_parameters(current_params: list, msg_list: List[str], option_type: List[type]) -> list:
  """Returns a list of valid parameters, given a list of input messages, errors and parameter types."""

  assert len(current_params) == len(msg_list) ==  len(option_type), "List input length mismatch"
  user_parameters = [None] * len(current_params)


  for i in range(len(msg_list)): # Go through every parameter
    while (type(user_parameters[i]) is not option_type[i]) and (user_parameters[i] != '~'): # Wait until either "skip" or correct input type
      user_parameters[i] = _user_input(msg_list[i], f"(skip w/ '~' or '--')") # Print setting

      # Below are checks to see if inputs are valid types
      type_bool = option_type[i] is bool and user_parameters[i] in ['true', 'false']
      type_int = option_type[i] is int and is_integer(user_parameters[i])
      type_float = option_type[i] is float and user_parameters[i].replace('.', '', 1).isdecimal()

      if (user_parameters[i] in skip_entry for skip_entry in ['', '~~~', '---']):
        user_parameters[i] = '~'
        print("Skipping...")

      elif '-' in user_parameters[i]: # Stops negative inputs
        print("Hyphens and minus signs (i.e. negative numbers) are not allowed, try again.")

      elif user_parameters[i] in ['island', 'toroid'] and type(user_parameters[i]) is str:
        pass # If this is supposed to be 'island' or 'toroid', do nothing to input. This could have been continue, if necessary.

      # If types are valid, evaluate (this converts the string to its correct type, and only if it is of that type)
      elif type_bool or type_int or type_float:
        user_parameters[i] = eval(user_parameters[i].capitalize()) # Capitalize in case of bool
        
      else:
        print(f"Invalid input, input was not of type '{param_type.__name__}'.")

  for i in range(len(user_parameters)):
    user_parameters[i] = current_params[i] if user_parameters[i] == '~' else user_parameters[i]

  print()
  return user_parameters





state = None # Initalize variable

while state != start_menu[-1]: #As long as not "quit"
  if state not in start_menu:
    quick_parameter_data = [params.world.north_south_length,
                            params.world.west_east_length,
                            params.rabbits.initial_size,
                            params.foxes.initial_size,
                            params.execution.max_steps,
                            params.execution.mode()]
    
    print(quick_param_msg.format(*quick_parameter_data))
  state = menu(start_menu)

  if state == start_menu[0]: #Display parameters
    print("ALL PARAMETERS:")
    print(params)

  if state == start_menu[1]: #Quick 
    # Assigns new values to the simulation
    current_params = [params.world.north_south_length,
                      params.world.west_east_length,
                      params.rabbits.initial_size,
                      params.foxes.initial_size,
                      params.execution.batch]

    new_params = input_parameters(current_params, quick_vars, quick_types)
    
    params.world.north_south_length, params.world.west_east_length, params.rabbits.initial_size, params.foxes.initial_size, params.execution.batch = new_params

    print()    
    state = None # This is only used to re-display the quick start parameters
    
  if state == start_menu[2]: #Advanced setup
    while state not in advanced_menu[-1]: #As long as not "done" or "go back"

      state = menu(advanced_menu)
      if state == advanced_menu[0]: #World
        current_params = [params.world.shape,
                          params.world.north_south_length,
                          params.world.west_east_length]
        new_params = input_parameters(current_params, adv_world, adv_world_types)
        params.world.shape, params.world.north_south_length, params.world.west_east_length = new_params
        
      if state == advanced_menu[1]: #Rabbit population
        current_params = [params.rabbits.initial_size,
                          params.rabbits.max_age,
                          params.rabbits.max_energy,
                          params.rabbits.metabolism,
                          params.rabbits.reproduction_probability,
                          params.rabbits.reproduction_min_age,
                          params.rabbits.reproduction_min_energy]
        new_params = input_parameters(current_params, adv_pop, adv_pop_types)
        
        params.rabbits.initial_size, params.rabbits.max_age, params.rabbits.max_energy, params.rabbits.metabolism = new_params[0:3]
        params.rabbits.reproduction_probability, params.rabbits.reproduction_min_age, params.rabbits.reproduction_min_energy = new_params[4:6]
      
      if state == advanced_menu[2]: #Fox population
        current_params = [params.foxes.initial_size,
                          params.foxes.max_age,
                          params.foxes.max_energy,
                          params.foxes.metabolism,
                          params.foxes.reproduction_probability,
                          params.foxes.reproduction_min_age,
                          params.foxes.reproduction_min_energy]
        new_params = input_parameters(current_params, adv_pop, adv_pop_types)
        
        params.foxes.initial_size, params.foxes.max_age, params.foxes.max_energy, params.foxes.metabolism = new_params[0:3]
        params.foxes.reproduction_probability, params.foxes.reproduction_min_age, params.foxes.reproduction_min_energy = new_params[4:6]
      
      if state == advanced_menu[3]: #Execution
        current_params = [params.execution.max_steps, params.execution.batch]
        params.execution.max_steps, params.execution.batch = input_parameters(current_params, adv_exe, adv_exe_types)
        
    state = None # This is only used to re-display the quick start parameters

  if state == start_menu[3]: #Run
    try:
      sim_data = sim.run(params)
      while state != reporting_menu[-1]: #As long as not "quit"
        state = menu(reporting_menu)
        
        if state == reporting_menu[0]: #Print summary
          report.print_summary(sim_data)
        if state == reporting_menu[1]: #Plot pop. size / time
          report.plot_pop_size(sim_data)
        if state == reporting_menu[2]: #Plot lifespan
          report.plot_lifespan(sim_data)
        if state == reporting_menu[3]: #Plot energy
          report.plot_energy(sim_data)
        if state == reporting_menu[4]: #Plot kills distribution
          report.plot_kills(sim_data)

    except AssertionError:
      # Metabolism isn't taken into account since we already do not allow negative numbers
      
      if not (params.world.north_south_length > 0 and params.world.west_east_length > 0):
        err = 'World lengths cannot be non-positive, please re-check parameters.' 

      elif not (params.world.area() >= params.rabbits.initial_size and params.world.area() >= params.foxes.initial_size):
        err = 'Initial population sizes must be smaller than world area, please re-check parameters.'

      else:
        err = 'Reproduction probabilities must be between 0 and 1.'
      
