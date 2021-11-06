import parameters
import time

"""
This module implements the simulation stage of the program.

WARNING: this is a mock implementation of the module.
"""

def run(parameters):
  """
  Runs a simulation with the given parameters and returns the data collected.
  """
  print(f"INFO: called function 'run' of module 'simulation'. This is a mock implementation.")

  # checks that preconditions on parameters are met
  print(' Checking parameters...',end='')
  assert 0 < parameters.world.north_south_length
  assert 0 < parameters.world.west_east_length
  assert 0 <= parameters.rabbits.initial_size <= parameters.world.area()
  assert 0 <= parameters.foxes.initial_size <= parameters.world.area()
  assert 0 <= parameters.rabbits.reproduction_probability <= 1
  assert 0 <= parameters.foxes.reproduction_probability <= 1
  assert 0 <= parameters.rabbits.metabolism
  assert 0 <= parameters.foxes.metabolism
  print('  everything is ok.')
  
  # the rest is for faking some computation using time.sleep while
  # displaying some progress indicator.
  
  width = 40
  steps = parameters.execution.max_steps
  delay = parameters.execution.step_delay
  print(' [' + 'simulation progress'.center(width) + ']')
  print(' [', end='', flush=True)
  filled = 0
  for count in range(1,steps + 1):
    time.sleep(delay)
    x = int(round(width * count / steps))
    if x - filled > 0:
      print('-' * (x - filled), end='', flush=True)
    filled = x
  print('] done',flush=True)
  
  # returns some dummy results
  return None 
