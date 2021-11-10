import parameters
import simulation as sim
import reporting as report
from typing import List

# Setting up menus
start_menu = ['display parameters', 'quick setup', 'advanced setup', 'run', 'quit']
advanced_menu = ['world', 'rabbits', 'foxes', 'execution', 'done']
reporting_menu = ['print summary', 'plot pop. size / time', 'plot lifespan', 'plot energy', 'plot kills distrubution', 'quit']

# Setting up variable changers
quick_vars = ['north/south length', 'west/east length', 'initial rabbits', 'initial foxes', 'batch (no visuals)']
quick_types = [int] * 4 + [bool]

world_vars = ['shape', 'north/south length', 'west/east length']
population_vars = ['initial size', 'max age', 'max energy', 'metabolism', 'reproduction probability', 'min reproduction age', 'min reproduction energy']
sim_vars = ['max steps', 'delay (in seconds) per step', 'batch (no visuals)']

params = parameters.Simulation()

quick_params = """world: {} by {} (north/south by west/east lengths)
initial rabbits: {}
initial foxes: {}
batch mode: {}"""



def _user_input(*msg: str):
  """Awaits an input and removes any excess spaces"""
  user = input(' '.join(msg) + ': ')
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

    state = _user_input("Awaiting input").lower() #Removes capitalization
    print()

    if is_integer(state) and float(state) - 1 in viable_states: #Handles floats/dots
        return menu_list[int(float(state)) - 1]
    elif state in menu_list:
      return state
    input("Invalid input, please try again (hit enter).") # Only printed if invalid state


def input_parameters(msg_list: List[str], option_type: List[type]) -> list:
  """Returns a list of valid parameters, given a list of input messages, errors and parameter types."""

  assert len(msg_list) ==  len(option_type), "List input length mismatch"
  parameter_list = [None] * len(msg_list)


  for i in range(len(msg_list)):
    while (type(parameter_list[i]) is not option_type[i]) and (parameter_list[i] != '~'):
      parameter_list[i] = _user_input(msg_list[i], f"(skip w/ '~' or '--')")
      type_bool = option_type[i] is bool and parameter_list[i].lower() in ['true', 'false']
      type_int = option_type[i] is int and is_integer(parameter_list[i])
      type_float = option_type[i] is float and parameter_list[i].replace('.', '', 1).isdecimal()

      if parameter_list[i] in ['', '~', '-', '--']:
        parameter_list[i] = '~'
        print("Skipping...")

      elif '-' in parameter_list[i]: # Stops negative inputs
        print("Hyphens and minus signs (i.e. negative numbers) are not allowed, try again.")

      elif parameter_list[i] in ['island', 'toroid'] and type(parameter_list[i]) is str:
        continue # if this is supposed to be island or toroid, just let it be that if it's that
      
      elif type_bool or type_int or type_float:
        parameter_list[i] = eval(parameter_list[i].capitalize())
      
      elif parameter_list[i] is not option_type[i]: # This is not run if input is supposed to be a string, otherwise it is
        print(f"Input '{parameter_list[i]}' is not of expected type '{option_type[i].__name__}'")

      else:
        print("Invalid input, try again.")

  print()
  return parameter_list





state = None # Initalize variable

while state != start_menu[-1]: #As long as not "quit"
  if state not in start_menu:
    print("QUICK PARAMETERS:")
    print(quick_params.format(params.world.north_south_length, params.world.west_east_length, params.rabbits.initial_size, params.foxes.initial_size, params.execution.batch))
  state = menu(start_menu)

  if state == start_menu[0]: #Display parameters
    print("ALL PARAMETERS:")
    print(params)

  if state == start_menu[1]: #Quick 
    # Assigns new values to the simulation
    params.world.north_south_length, params.world.west_east_length, params.rabbits.initial_size, params.foxes.initial_size, params.execution.batch = input_parameters(quick_vars, quick_types) 
    
    state = None # This is only used to re-display the quick start parameters
    
  if state == start_menu[2]: #Advanced setup
    while state != advanced_menu[-1]: #As long as not "done"

      state = menu(advanced_menu)
      if state == advanced_menu[0]: #World
        pass
      if state == advanced_menu[1]: #Rabbit population:
        pass
      if state == advanced_menu[2]: #Fox population:
        pass
      if state == advanced_menu[3]: #Execution:
        pass
  state = None

  if state == start_menu[3]: #Run
    sim_data = sim.run(params)
    while state != reporting_menu[-1]: #As long as not "quit"
      state = menu(reporting_menu)
      
      if state == reporting_menu[0]: #Print summary
        report.print_summary
      if state == reporting_menu[1]: #Plot pop. size / time
        report.plot_pop_size
      if state == reporting_menu[2]: #Plot lifespan
        report.plot_lifespan
      if state == reporting_menu[3]: #Plot energy
        report.plot_energy
      if state == reporting_menu[4]: #Plot kills distribution
        report.plot_kills
