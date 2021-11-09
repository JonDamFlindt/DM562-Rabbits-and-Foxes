import parameters as param
import simulation as sim
import reporting as report
import typing
import json
# Setting up menus
start_menu = ['Display parameters', 'Quick setup', 'Advanced setup', 'Run', 'Quit']
advanced_menu = ['World', 'Rabbit population', 'Fox population', 'Execution', 'Done']
reporting_menu = ['Print summary', 'Plot pop. size / time', 'Plot lifespan', 'Plot energy', 'Plot kills distrubution', 'Plot all', 'Quit']

config_file = 'parameters.json'

quick_params = """QUICK PARAMETERS:
North/South length (height, positive int): {}
West/East length (width, positive int): {}
[Fox] Initial size (positive int): {}
[Rabbit] Initial size (positive int): {}
Visuals (True/False): {}
"""

def menu(menu_list: typing.List[str]) -> str:
    """Menu function
    Prints a list of options which the user can choose as input given a list.
    Precondition: menu_list is a list of strings.
    """
    state = None # Initialize variable
    
    viable_states = range(len(menu_list)) # Get viable states from the menu
       
    while state not in viable_states:
        print("Action selection:")
        for option in viable_states: # Prints all menu options
            print(str(option + 1) + '.', menu_list[option])
        
        state = input("Awaiting input: ").replace('.', '').split(' ')
        state = ' '.join([word for word in state if word != '']).capitalize()
        # Above handles any extra spaces the user may insert into the input.
        
        print()
        try:
            state = int(state) - 1 # Raises ValueError if state is not int
            if state in viable_states:
                return menu_list[state]
        except ValueError: # Checks if state is string in menu
            if state in menu_list:
                return state
            state = None
        
        input("Invalid input, please try again (hit enter).\n") # Only printed if invalid state

state = None # Default state

while state != start_menu[-1]: # As long as not "Quit"
  if state not in start_menu:
    with open(config_file) as file:
      pass
    print(quick_params)
  state = menu(start_menu)

  if state == start_menu[0]: #Display parameters
    with open(config_file) as file:
      parameters = json.load(file)
    for category in parameters:
      print(f'[{category}]')
      for setting in parameters[category]:
        print(f'{setting}: {parameters[category][setting]}')
      print()


  if state == start_menu[1]: #Quick setup
    with open(config_file) as parameters:
      pass

  if state == start_menu[2]: #Advanced setup
    while state != advanced_menu[-1]: # As long as not "Done/go back"
      with open(config_file) as parameters:
        pass

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
    with open(config_file) as parameters:
      pass
        
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
