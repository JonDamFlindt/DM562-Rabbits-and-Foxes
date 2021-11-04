import parameters as param
import simulation as sim
import reporting as report
# Setting up menus
start_menu = ['Display parameters', 'Quick setup', 'Advanced setup', 'Run', 'Quit']
advanced_menu = ['World', 'Rabbit population', 'Fox population', 'Execution', 'Done/Go back']
reporting_menu = ['Print summary', 'Plot pop. size / time', 'Plot lifespan', 'Plot energy', 'Plot kills distrubution', 'Plot all', 'Quit']

#Setting up dynamic strings
advanced_params = """
Advanced parameters:

[World]
Shape ('toroid'/'island'): {}
North/South length (height, positive): {}
West/East length (width, positive): {}

[Fox]
Initial size: {}
Metabolism (energy/step): {}
Maximum energy: {}
Maximum age: {}
Mating probability: {}
Minimum mating energy: {}
Minimum mating age: {}

[Rabbit]
Initial size: {}
Metabolism (energy/step): {}
Maximum energy: {}
Maximum age: {}
Mating probability: {}
Minimum mating energy: {}
Minimum mating age: {}

[Simulation]
Duration: {}
Step delay (seconds): {}
Visuals: {}
"""

quick_params = """
World height (North/South length): {}
World width (East/West length): {}
Initial fox pop size: {}
Initial rabbit pop size: {}
Simulation model: {}
"""

def menu(menu_list: typing.List[str]) -> int:
    """Menu function
    Prints a list of options which the user can choose as input given a list.
    Precondition: menu_list is a list of strings.
    """
    state = 0 # Initialize variable
    
    viable_states = range(len(menu_list)) # Get viable states from the menu
       
    while state - 1 not in viable_states: # state - 1, since all states range from 1 to len(menu_list) + 1
        print("Action selection:")
        for option in viable_states:
            print(str(option + 1) + '.', menu_list[option])
        state = input("Awaiting input: ").replace('.', '')
        try:
            state = int(state)
            if state - 1 in viable_states:
                return state
        except (ValueError, TypeError):
            state = 0
        
        input("\nInput must be an integer, please try again (hit enter).\n")

state = 0 # Default state, only assigned manually, cannot be user input

while True:
  if state not in range(1, 1 + len(start_menu)):
    with open('parameters.csv') as parameters:
      pass
    print(quick_params)
  state = menu(start_menu)

  if state == 1: #Display parameters
    with open('parameters.csv') as parameters:
      pass
    print(advanced_params)

  if state == 2: #Quick setup
    with open('parameters.csv', mode='w') as parameters:
      pass
    state = 0

  if state == 3: #Advanced setup
    with open('parameters.csv', mode='w') as parameters:
      pass
    while True:
        state = menu(advanced_menu)
        if state == 1: #World
          pass
        if state == 2: #Rabbit population
          pass
        if state == 3: #Fox population
          pass
        if state == 4: #Execution
          pass
        if state == 5: #Done/go back
          state = 0
          break

  if state == 4: #Run
    with open('parameters.csv') as parameters:
      pass
        
    while True:
      state = menu(reporting_menu)
            
      if state == 1: #Print summary
        pass
      if state == 2: #Plot pop. siz e/ time
        pass
      if state == 3: #Plot lifespan
        pass
      if state == 4: #Plot energy
        pass
      if state == 5: #Plot kills distribution
        pass
      if state == 6: #Plot all
        pass            
      if state == 7: #Quit
        state = 5
        break
  
  if state == 5: #Quit
    break
