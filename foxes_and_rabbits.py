import parameters as param
import simulation as sim
import reporting as report
from typing import List

# Setting up menus
start_menu = ['display parameters', 'quick setup', 'advanced setup', 'run', 'quit']
advanced_menu = ['world', 'rabbits', 'foxes', 'execution', 'done']
reporting_menu = ['print summary', 'plot pop. size / time', 'plot lifespan', 'plot energy', 'plot kills distrubution', 'quit']

quick_params = """QUICK PARAMETERS:
North/South length (height, positive int): {}
West/East length (width, positive int): {}
[Fox] Initial size (positive int): {}
[Rabbit] Initial size (positive int): {}
Visuals (True/False): {}
"""

"""ADVANCED PARAMETERS:
{}
{}
{}
{}
{}
{}
"""

def menu(menu_list: List[str]) -> str:
  """Menu function
  Prints a list of options which the user can choose as input given a list.
  """
  state = None # Initialize variable
  
  viable_states = range(len(menu_list)) # Get viable states from the menu
     
  while state not in viable_states:
    print("Action selection:")
    for option in viable_states: # Prints all menu options
      print(str(option + 1) + '.', menu_list[option].capitalize())
    
    state = input("Awaiting input: ").lower().replace('.', '').split(' ') # Handles any extra spaces in input
    state = ' '.join([word for word in state if word != ''])
    print()

    
    try: # Reasoning for try/except here is that even something like 0.2 is not a viable state, and we allow "1." as a valid input.
      state = int(state) - 1 # Raises ValueError if state is not int
      if state in viable_states:
        return menu_list[state]
    
    except ValueError: # Checks if state is string in menu
      if state in menu_list:
        return state
        
  input("Invalid input, please try again (hit enter).\n") # Only printed if invalid state

state = None # Default state

while state != start_menu[-1]: # As long as not "quit"
  if state not in start_menu:
    print(quick_params)
  state = menu(start_menu)

  if state == start_menu[0]: #Display parameters
    print()


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
    sim_data = sim.Run()
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
