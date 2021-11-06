"""
This module provides functions for analysing and reporting results of a simulation.

WARNING: this is a mock implementation of the module.
"""

def print_summary(results):
  """
  Prints a summary of the simulation results and basic statistics.
  """
  _print_info(print_summary)

def plot_pop_size(results):
  """
  Plots population sizes against time. 
  """
  _print_info(plot_pop_size)

def plot_lifespan(results):
  """
  Plots lifespans across population idividuals. 
  """
  _print_info(plot_lifespan)

def plot_energy(results):
  """
  Plots the total energry over the life of eah individual. 
  """
  _print_info(plot_energy)

def plot_kills(results):
  """
  Displays the distribution of kills.
  """
  _print_info(plot_kills)


def plot_all(results):
  """
  Displays the distribution of kills.
  """
  _print_info(plot_kills)  
  
def _print_info(f):
  print(f"INFO: called function '{f.__name__}' of module 'reporting'. This is a mock implementation.")
