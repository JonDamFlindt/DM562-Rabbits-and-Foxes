import parameters as param
import simulation as sim
import reporting as report
import typing
import csv
# Setting up menus
start_menu = ['Display parameters', 'Quick setup', 'Advanced setup', 'Run', 'Quit']
advanced_menu = ['World', 'Rabbit population', 'Fox population', 'Execution', 'Done/Go back']
reporting_menu = ['Print summary', 'Plot pop. size / time', 'Plot lifespan', 'Plot energy', 'Plot kills distrubution', 'Plot all', 'Quit']

#Setting up dynamic strings -- note that these in entirety should be in a .json file and parsed.
#Forgot if .json files use "" or '', but we'll figure it out by testing.
advanced_params = """ADVANCED PARAMETERS:
[World]
Shape ('toroid'/'island'): {}
North/South length (height, positive int): {}
West/East length (width, positive int): {}

[Fox]
Initial size (positive int): {}
Metabolism (energy/step, positive int): {}
Maximum energy (positive int): {}
Maximum age (positive int): {}
Mating probability (float between 0 and 1): {}
Minimum mating energy (positive int): {}
Minimum mating age (positive int): {}

[Rabbit]
Initial size(positive int): {}
Metabolism (energy/step, positive int): {}
Maximum energy (positive int): {}
Maximum age (positive int): {}
Mating probability (float between 0 and 1): {}
Minimum mating energy (positive int): {}
Minimum mating age (positive int): {}

[Simulation]
Duration/iterations/steps (positive int): {}
Step delay (seconds, positive float): {}
Visuals (True/False): {}
"""

quick_params = """QUICK PARAMETERS:
North/South length (height, positive int): {}
West/East length (width, positive int): {}
[Fox] Initial size (positive int): {}
[Rabbit] Initial size (positive int): {}
Visuals (True/False): {}
"""

def menu(menu_list: typing.List[str]) -> int:
    """Menu function
    Prints a list of options which the user can choose as input given a list.
    Precondition: menu_list is a list of strings.
    """
    state = -1 # Initialize variable
    
    viable_states = range(len(menu_list)) # Get viable states from the menu
       
    while state not in viable_states:
        print("Action selection:")
        for option in viable_states:
            print(str(option + 1) + '.', menu_list[option])
        state = input("Awaiting input: ").capitalize().replace('.', '')
        print()
        try:
            state = int(state) - 1
            if state in viable_states:
                return menu_list[state]
        except (ValueError, TypeError):
            if state in menu_list:
                return state
            state = -1
        
        input("Invalid input, please try again (hit enter).\n")

state = -1 # Default state, only assigned manually, cannot be user input

while True:
  if state not in start_menu:
    with open('parameters.json') as parameters:
      pass
    print(quick_params)
  state = menu(start_menu)

  if state == start_menu[0]: #Display parameters
    with open('parameters.json') as parameters:
      pass
    print(advanced_params)

  if state == start_menu[1]: #Quick setup
    with open('parameters.json') as parameters:
      pass
    state = -1

  if state == start_menu[2]: #Advanced setup
    with open('parameters.json') as parameters:
      pass
    
    while True:
      state = menu(advanced_menu)
      if state == advanced_menu[0]: #World
        pass
      if state == advanced_menu[1]: #Rabbit population:
        pass
      if state == advanced_menu[2]: #Fox population:
        pass
      if state == advanced_menu[3]: #Execution:
        pass
      if state == advanced_menu[4]: #Done/go back:
        state = -1
        break

  if state == start_menu[3]: #Run
    with open('parameters.json') as parameters:
      pass
        
    while True:
      state = menu(reporting_menu)
            
      if state == reporting_menu[0]: #Print summary
        pass
      if state == reporting_menu[1]: #Plot pop. siz e/ time
        pass
      if state == reporting_menu[2]: #Plot lifespan
        pass
      if state == reporting_menu[3]: #Plot energy
        pass
      if state == reporting_menu[4]: #Plot kills distribution
        pass
      if state == reporting_menu[5]: #Plot all
        pass            
      if state == reporting_menu[6]: #Quit
        break #Note that reporting_menu[6] == start_menu[4]
  
  if state == start_menu[4]: #Quit
    break #Note that reporting_menu[6] == start_menu[4] == "Quit"
