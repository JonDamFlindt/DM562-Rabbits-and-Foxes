class Population:
  def __init__(self, name: str, size_init: int, metabolism: int, max_energy: int, max_age: int, mating_prob: float, mating_min_energy: int, mating_min_age: int):
    self.name = name
    self.size = size_init
    self.metabolism = metabolism
    self.max_energy = max_energy
    self.max_age = max_age
    self.mating_prob = mating_prob
    self.mating_min_energy = mating_min_energy
    self.mating_min_age = mating_min_age
    
    
class World:
  def __init__(self, ns_length: int, ew_length: int, is_toroid: bool):
    self.height = ns_length
    self.width = ew_length
    self.is_toroid = is_toroid
  
class Execution:
  def __init__(self, max_steps: int, step_delay: float, batch: bool):
    self.max_steps = max_steps
    self.step_delay = step_delay
    self.batch = batch
  
class Simulation:
  def __init__(self, world, rabbits, foxes, execution):
    pass
