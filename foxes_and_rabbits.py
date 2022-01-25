import parameters
import simulation as sim
import reporting as report
from typing import List, Union, Tuple
import sys

# Setting up menus
start_menu = ['display parameters', 'quick setup', 'advanced setup', 'run', 'quit']
advanced_menu = ['world', 'rabbits', 'foxes', 'execution', 'done']
reporting_menu = ['print summary', 'plot pop. size / time', 'plot lifespan', 'plot energy', 'plot kills distrubution', 'quit']

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
    print("\nSelection:")
    for option in viable_states: #Prints all menu options
      print(str(option + 1) + '.', menu_list[option].capitalize())

    user = _user_input() #Basically just input() that handles spaces
    print()

    if is_integer(user) and float(user) - 1 in viable_states: #Handles floats/dots
        state = menu_list[int(float(user)) - 1]
  
    elif user in menu_list:
      state = user

    else:
      input("Invalid input, please try again (hit enter).") # Only printed if invalid state

  return state


def bool_input(true_option: str, false_option: str, msg: str) -> bool:
  """Input method for parameters of bool values. First bool should be the True statement, second one should be False."""
  print(f'{msg}\n')
  user = menu([true_option, false_option])
  return user == true_option
  

def int_input(user_msg: str, lower_limit: int, upper_limit: int) -> int:
  """Input method for parameters of integer values."""
  user = 'spam'
  while not user.isdigit() or not lower_limit <= int(user) <= upper_limit:  
    user = _user_input(user_msg + f" (between {lower_limit} and {upper_limit})")
    if not user.isdigit() or not lower_limit <= int(user) <= upper_limit:
      print(f"Input must be an integer between {lower_limit} and {upper_limit}, try again.")
  return int(user)


def float_input() -> float:
  """Input method for parameters of floating point values."""
  user = 'spam'
  while not user.replace('.','',1).isdigit() or not 0 <= float(user) <= 1:
    # Between 0 and 1 since this is only used for reproduction  
    user = _user_input('Please enter the reproduction probability of the population as a percentage between 0 and 1')
    if not user.replace('.','',1).isdigit() or not 0 <= float(user) <= 1:
      print(f"Input must be a decimal number (float) between 0 and 1 (i.e. a percentage), try again.")
  return float(user)


def update_animal(animal: parameters.Population) -> None:
  """Function used to update population parameters for the animals of the simulation."""
  animal.initial_size = int_input('Please enter an initial size of the population', 0, params.world.area())
  animal.max_age = int_input('Please enter the max age for the population', 0, 500)
  animal.max_energy = int_input('Please enter the maximum amount of energy that a member of the population can attain', 0, 100)
  animal.metabolism = int_input('Please enter the metabolism of the population', 1, 100)
  animal.reproduction_probability = float_input()
  animal.reproduction_min_age = int_input('Please enter the minimum age for reproduction for the population', 0, animal.max_age)
  animal.reproduction_min_energy = int_input('Please enter the minimum required energy for reproduction', 0, animal.max_energy)


def set_execution() -> None:
  """Used to update the execution settings for the simulation."""
  params.execution.max_steps = int_input('Please enter the maximum amount of simulation steps', 1, round(sys.maxsize**(1/4)/1000)*1000)
  params.execution.batch = bool_input('batch', 'visual', 'Please choose a simulation mode')

state = None # Initalize variable

while state != start_menu[-1]: #As long as not "quit"
  if state not in start_menu:
    print(quick_param_msg.format(params.world.north_south_length,
                            params.world.west_east_length,
                            params.rabbits.initial_size,
                            params.foxes.initial_size,
                            params.execution.max_steps,
                            params.execution.mode()))
  state = menu(start_menu)

  if state == start_menu[0]: #Display parameters
    print("ALL PARAMETERS:")
    print(params)

  elif state == start_menu[1]: #Quick 
    # Assigns new values to the simulation
    params.world.north_south_length = int_input('Please enter a north/south length for the world', 1, 500)
    params.world.west_east_length = int_input('Please enter a west/east length for the world', 1, 500)
    params.rabbits.initial_size = int_input('Please enter an initial size of the rabbit population', 0, params.world.area())
    params.foxes.initial_size = int_input('Please enter an initial size of the fox population', 0, params.world.area())
    set_execution()

    print()
    state = None # This is only used to re-display the quick start parameters
    
  elif state == start_menu[2]: #Advanced setup
    while state not in advanced_menu[-1]: #As long as not "done" or "go back"

      state = menu(advanced_menu)
      if state == advanced_menu[0]: #World
        params.world.is_toroid = bool_input('loop','walls', 'Should the world loop or have walls?')
        params.world.north_south_length = int_input('Please enter a north/south length for the world', 1, 500)
        params.world.west_east_length = int_input('Please enter a west/east length for the world', 1, 500)
        
      elif state == advanced_menu[1]: #Rabbit population
        update_animal(params.rabbits)
              
      elif state == advanced_menu[2]: #Fox population
        update_animal(params.foxes)
      
      elif state == advanced_menu[3]: #Execution
        set_execution()
        
    state = None # This is only used to re-display the quick start parameters

  elif state == start_menu[3]: #Run
    sim_data = sim.run(params)
    while state != reporting_menu[-1]: #As long as not "quit"
      state = menu(reporting_menu)
        
      if state == reporting_menu[0]: #Print summary
        report.print_summary(sim_data)
      elif state == reporting_menu[1]: #Plot pop. size / time
        report.plot_pop_size(sim_data)
      elif state == reporting_menu[2]: #Plot lifespan
        report.plot_lifespan(sim_data)
      elif state == reporting_menu[3]: #Plot energy
        report.plot_energy(sim_data)
      elif state == reporting_menu[4]: #Plot kills distribution
        report.plot_kills(sim_data)
      
