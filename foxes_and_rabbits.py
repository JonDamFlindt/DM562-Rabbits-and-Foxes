import parameters as param
import simulation as sim
import reporting as report

setup_type = None

while True:
  while setup_type not in ['quick', 'advanced', 'cancel', 'exit']: # while-loop to ensure valid setup choice
    print(f"Quick parameter setup:\n{}\n{}\n{}")
    print("")
    setup_type = input("Please choose whether you want to use quick setup or advanced setup, or exit the program:\n").lower()
    if setup_type not in ['quick', 'advanced', 'cancel', 'exit']:
      input("Unrecognized command, please try again (hit enter).")
    
   
  if setup_type in ['cancel', 'exit']:
    print(f"Terminating the program.")
    break
  
  if setup_type == 'quick':
    pass
  
  if setup_type == 'advanced':
    pass
  

