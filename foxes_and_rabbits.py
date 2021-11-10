import parameters
import simulation as sim
import reporting as report
from typing import List

# Setting up menus
start_menu = ['display parameters', 'quick setup', 'advanced setup', 'run', 'quit']
advanced_menu = ['world', 'rabbits', 'foxes', 'execution', 'done']
reporting_menu = ['print summary', 'plot pop. size / time', 'plot lifespan', 'plot energy', 'plot kills distrubution', 'quit']

params = parameters.Simulation()

quick_params = """QUICK PARAMETERS:
world: {} (north/south by west/east lengths)
initial rabbits: {}
initial foxes: {}
batch mode: {}
"""

def menu(menu_list: List[str]) -> str:
  """Menu function:
  Prints a list of options which the user can choose as input given a list.
  User input is either a number (e.g. "1." or "1") or a string (e.g. "Done")
  """

  state = None # Initialize variable
  viable_states = range(len(menu_list)) # Get viable states from the menu

  while state not in viable_states:
    print("\nAction selection:")
    for option in viable_states: # Prints all menu options
      print(str(option + 1) + '.', menu_list[option].capitalize())


    state = input("Awaiting input: ").lower() #Removes capitalization
    state = ' '.join([word for word in state.split(' ') if word != '']) # Handles any extra spaces in input

    if state.replace('.','').isdecimal() and float(state) == int(float(state)) and int(float(state)) in viable_states: # Handles floats/dots
      return menu_list[int(float(state)) - 1]
    elif state in menu_list:
      return state
    input("\nInvalid input, please try again (hit enter).") # Only printed if invalid state

state = None # Default state
while state != start_menu[-1]: # As long as not "quit"
  if state not in start_menu:
    print(quick_params.format(params.world, params.rabbits.initial_size, params.foxes.initial_size, params.execution.batch))
  state = menu(start_menu)

  if state == start_menu[0]: #Display parameters
    print("\nALL PARAMETERS:")
    print(params)

  if state == start_menu[1]: #Quick setup
    pass

  if state == start_menu[2]: #Advanced setup
    while state != advanced_menu[-1]: # As long as not "Done/go back"

      state = menu(advanced_menu)
      if state == advanced_menu[0]: #World
        pass
      if state == advanced_menu[1]: #Rabbit population:
        pass
      if state == advanced_menu[2]: #Fox population:
        pass
      if state == advanced_menu[3]: #Execution:
        pass

  if state == start_menu[3]: #Run
    sim_data = sim.run(params)
    while state != reporting_menu[-1]: # As long as not "Quit"
      state = menu(reporting_menu)
      
      if state == reporting_menu[0]: #Print summary
        pass
      if state == reporting_menu[1]: #Plot pop. size / time
        pass
      if state == reporting_menu[2]: #Plot lifespan
        pass
      if state == reporting_menu[3]: #Plot energy
        pass
      if state == reporting_menu[4]: #Plot kills distribution
        pass
      if state == reporting_menu[5]: #Plot all
        pass
