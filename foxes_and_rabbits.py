import parameters
import simulation as sim
import reporting as report
from typing import List

# Setting up menus
start_menu = ['display parameters', 'quick setup', 'advanced setup', 'run', 'quit']
advanced_menu = ['world', 'rabbits', 'foxes', 'execution', 'done']
reporting_menu = ['print summary', 'plot pop. size / time', 'plot lifespan', 'plot energy', 'plot kills distrubution', 'quit']

# Setting up variable changers
quick_vars = ['north/south length (positive int)', 'west/east length (positive int)', 'initial rabbits (int, less than world area)', 'initial foxes (int, less than world area)', 'max steps (int)', 'batch mode (bool)']
adv_world = ['toroidal (bool)', 'north/south length (positive int)', 'west/east length (positive int)']
adv_pop = ['initial size (int, less than world area)', 'max age (int)', 'max energy (int)', 'metabolism (int)', 'reproduction probability (float between 0 and 1)', 'min reproduction age (int)', 'min reproduction energy (int)']
adv_exe = ['max steps (int)', 'batch mode (bool)']


quick_param_msg = """QUICK PARAMETERS:
world: {} by {} (n/s by w/e)
initial rabbits: {}
initial foxes: {}
max steps: {}
mode: {}"""


params = parameters.Simulation()



def _user_input(msg: str = 'Awaiting input'):
  """Awaits an input and removes any excess spaces."""
  user = input(msg + ': ').lower() #User input, removes capitalization
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

  state = None # Initialize state
  viable_states = range(len(menu_list)) #Get viable states from the menu

  while state not in menu_list:
    print("\nAction selection:")
    for option in viable_states: #Prints all menu options
      print(str(option + 1) + '.', menu_list[option].capitalize())

    user = _user_input()
    print()

    if is_integer(user) and float(user) - 1 in viable_states: #Handles floats/dots
        state = menu_list[int(float(user)) - 1]
  
    elif user in menu_list:
      state = user

    else:
      input("Invalid input, please try again (hit enter).") # Only printed if invalid state

  return state


def input_parameters(current_params: list, msg_list: List[str]) -> list:
  """Returns a list of valid parameters, given a list of current parameters and input messages."""

  assert len(current_params) == len(msg_list), "List input length mismatch"
  user_parameters = [None] * len(current_params)
  print("Parameter setup, skip parameter change by pressing enter or w/ '~' or '-')")


  for i in range(len(msg_list)): # Go through every parameter
    current_type = type(current_params[i])
    while type(user_parameters[i]) is not current_type and (user_parameters[i] != '~'): # Wait until either "skip" or correct input type
      user_parameters[i] = _user_input(msg_list[i]) # Print setting

      # Below are checks to see if inputs are valid types
      type_bool = current_type is bool and user_parameters[i] in ['true', 'false']
      type_int = current_type is int and is_integer(user_parameters[i])
      type_float = current_type is float and user_parameters[i].replace('.', '', 1).isdecimal()

      if user_parameters[i] in ['', '~', '-']:
        user_parameters[i] = '~'
        print("Skipping...")

      elif '-' in user_parameters[i]: # Stops negative inputs
        print("Hyphens and minus signs (i.e. negative numbers) are not allowed, try again.")

      # If types are valid, evaluate (this converts the string to its correct type, and only if it is of that type)
      elif type_bool or type_int or type_float:
        user_parameters[i] = eval(user_parameters[i].capitalize()) # Capitalize in case of bool
        if type_float:
          user_parameters[i] = float(user_parameters[i]) # In case float input is "1" or "0" as ints
        
      else:
        print(f"Invalid input, not of type '{current_type.__name__}'.")

  for i in range(len(user_parameters)):
    user_parameters[i] = current_params[i] if user_parameters[i] == '~' else user_parameters[i]

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
                      params.execution.max_steps,
                      params.execution.batch]

    new_params = input_parameters(current_params, quick_vars)
    
    params.world.north_south_length, params.world.west_east_length = new_params[:2]
    params.rabbits.initial_size, params.foxes.initial_size = new_params[2:4]
    params.execution.max_steps, params.execution.batch = new_params[4:]

    print()
    state = None # This is only used to re-display the quick start parameters
    
  if state == start_menu[2]: #Advanced setup
    while state not in advanced_menu[-1]: #As long as not "done" or "go back"

      state = menu(advanced_menu)
      if state == advanced_menu[0]: #World
        current_params = [params.world.is_toroid,
                          params.world.north_south_length,
                          params.world.west_east_length]
        new_params = input_parameters(current_params, adv_world)
        params.world.is_toroid, params.world.north_south_length, params.world.west_east_length = new_params
        
      if state == advanced_menu[1]: #Rabbit population
        current_params = [params.rabbits.initial_size,
                          params.rabbits.max_age,
                          params.rabbits.max_energy,
                          params.rabbits.metabolism,
                          params.rabbits.reproduction_probability,
                          params.rabbits.reproduction_min_age,
                          params.rabbits.reproduction_min_energy]
        new_params = input_parameters(current_params, adv_pop)
        
        params.rabbits.initial_size, params.rabbits.max_age, params.rabbits.max_energy, params.rabbits.metabolism = new_params[:4]
        params.rabbits.reproduction_probability, params.rabbits.reproduction_min_age, params.rabbits.reproduction_min_energy = new_params[4:]
      
      if state == advanced_menu[2]: #Fox population
        current_params = [params.foxes.initial_size,
                          params.foxes.max_age,
                          params.foxes.max_energy,
                          params.foxes.metabolism,
                          params.foxes.reproduction_probability,
                          params.foxes.reproduction_min_age,
                          params.foxes.reproduction_min_energy]
        new_params = input_parameters(current_params, adv_pop)
        
        params.foxes.initial_size, params.foxes.max_age, params.foxes.max_energy, params.foxes.metabolism = new_params[:4]
        params.foxes.reproduction_probability, params.foxes.reproduction_min_age, params.foxes.reproduction_min_energy = new_params[4:]
      
      if state == advanced_menu[3]: #Execution
        current_params = [params.execution.max_steps, params.execution.batch]
        params.execution.max_steps, params.execution.batch = input_parameters(current_params, adv_exe)
        
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
      print('Invalid parameters detected, please redo setup.')
      state = None
      
