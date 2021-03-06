from __future__ import annotations
# Above is just to allow Optional[Animal], otherwise it raises a NameError as the Animal class doesn't yet exist
import parameters
import random
from typing import Type, Tuple, Optional



class Patch:
   min_grass_growth = 1
   max_grass_growth = 4
   max_grass_amount = 30
   
   def __init__(self, x: int, y: int):
      self._coords = (x,y)
      self._Animals = []
      self._grass = round(random.uniform(0,1) * Patch.max_grass_amount)
      
   def coordinates(self) -> Tuple[int, int]:
      """Returns the coordinates of the given patch."""
      return self._coords

   def grass(self) -> int:
      """Returns the amount of grass on the patch."""
      return self._grass

   def animals(self) -> list:
      """Returns a list of the animals on the patch."""
      copy = self._Animals
      return copy
   
   def tick(self):
      """
      Progresses time for the patch in the simulation.
      """
      self._grass += round(random.uniform(Patch.min_grass_growth, Patch.max_grass_growth))
      if self._grass > Patch.max_grass_amount:
         self._grass = Patch.max_grass_amount

   def _check_alive(self, animal_class) -> bool:
      """ Auxiliary method for checking if an animal type on a given patch is alive. """
      alive = False
      i = 0
      while i < len(self._Animals) and not alive:
         if self._Animals[i].is_alive() and isinstance(self._Animals[i], animal_class):
            alive = True
         else:
            i += 1
      return alive

   def has_alive_fox(self) -> bool:
      """Checks whether or not the patch has an alive fox on it."""
      return self._check_alive(Fox)

   def has_alive_rabbit(self) -> bool:
      """Checks whether or not the patch has an alive rabbit on it."""
      return self._check_alive(Rabbit)

   def add(self, animal: Animal):
      """
      Adds the given animal to the patch
      """
      if animal not in self._Animals:
         self._Animals.append(animal)

   def remove(self, animal: Animal):
      """
      Removes the given animal from the patch, if it is on the patch.
      """
      try:
         self._Animals.remove(animal)
      except ValueError:
         pass



class Animal:
   """
   Generic fundamental animal superclass of the simulation,
   see subclasses "Fox" and "Rabbit".
   """
   def __init__(self, pop: parameters.Population, patch: Patch, energy: int, age: int):
      self._pop = pop
      self._alive = True
      self._age = age
      self._energy = energy
      self._patch = patch
      self._patch.add(self)

   def age(self) -> int:
      """ Returns the animal's current age."""
      return self._age

   def energy(self) -> int:
      """ Returns the animal's current energy."""
      return self._energy

   def patch(self) -> Patch:
      """ Returns the animal's last/current coordinates. """
      return self._patch

   def is_alive(self) -> bool:
      """ Returns 'True' if the animal is still alive."""
      return self._alive

   def can_reproduce(self) -> bool:
      rep_req_energy = self.energy() >= self._pop.reproduction_min_energy
      rep_req_age = self.age() >= self._pop.reproduction_min_age
      return self.is_alive() and rep_req_energy and rep_req_age

   def tick(self):
      """
      Ages the animal, expends its energy and kills it if it fails meeting survival requirements given by simulation parameters.
      """
      self._age += 1
      self._energy -= self._pop.metabolism
      if self._age >= self._pop.max_age or self._energy <= 0:
         self._alive = False
         self._patch.remove(self)         

   def move_to(self, patch: Patch):
      """Moves the animal to the given patch."""
      if self.is_alive():
         self._patch.remove(self)
         self._patch = patch
         self._patch.add(self)

   def same_species_in(self, patch: Patch) -> bool:
      """Returns 'True' if the given patch has an animal of the same type."""
      raise NotImplementedError()

   def predators_in(self, patch: Patch) -> bool:
      """Returns 'True' if the given patch has a predator of the current animal."""
      raise NotImplementedError()

   def reproduce(self, newborn_patch: Patch, rep_cost_rate) -> Optional[Animal]:
      """
      General method for reproduction of a species.
      Should be called from a descendant of Animal, i.e. not an Animal object, hence the __name__ check.
      """
      if self.can_reproduce() and random.uniform(0,1) < self._pop.reproduction_probability and type(self).__name__ != "Animal":
         newborn = self.__class__(self._pop, newborn_patch, 0) # The "clever!" line.
         self._energy -= self._pop.reproduction_min_energy * rep_cost_rate
         newborn_patch.add(newborn)
         baby = newborn
      else:
         baby = None
      return baby


class Fox(Animal):
   """
   The class representing a single fox in the simulation.
   """
   reproduction_cost_rate = 0.85
   food_energy_per_unit = 15

   def __init__(self, pop: parameters.Population, patch: Patch, age: int = 0):
      energy = round(0.7 * pop.max_energy)
      super().__init__(pop, patch, energy, age)

   def is_alive(self):
      """See 'is_alive()' of parent 'Animal'."""
      return super().is_alive()

   def feed(self):
      """Feed method for Fox, increases its energy by eating rabbits."""
      if self.is_alive() and self._patch.has_alive_rabbit() and self.energy() < self._pop.max_energy:
         food = False
         i = 0
         while not food: # i  cannot go out of index, since we know there is a rabbit.
            if isinstance(self._patch._Animals[i], Rabbit) and self._patch._Animals[i].is_alive():
               food = True
            else:
               i += 1
         

         self._patch._Animals[i].kill() # Kill the rabbit
         self._energy += self.food_energy_per_unit
         if self._energy > self._pop.max_energy:
            self._energy = self._pop.max_energy
         

   def reproduce(self, newborn_patch: Patch) -> Optional[Fox]:
      """Reproduction method for the Fox class."""
      return super().reproduce(newborn_patch, Fox.reproduction_cost_rate)  

   def same_species_in(self, patch: Patch) -> bool:
      """Checks if there are any foxes in the given patch."""
      return patch.has_alive_fox()
      
   def predators_in(self, patch: Patch) -> bool:
      """
      Checks if there are any predators in the given patch.
      Always returns false as there are no fox predators.
      """
      return False



class Rabbit(Animal):
   """
   The class representing a single rabbit in the simulation.
   """

   reproduction_cost_rate = 0.85
   feeding_metabolism_rate = 2.5
   
   def __init__(self, pop: parameters.Population, patch: Patch, age: int = 0):
      self._killed = False
      energy = round(0.25 * pop.max_energy)
      super().__init__(pop, patch, energy, age)

   def was_killed(self) -> bool:
      """Returns whether or not the rabbit was killed by a predator"""
      return self._killed

   def kill(self):
      """Kills the rabbit and removes it from the patch."""
      self._killed = True
      self._patch.remove(self)

   def is_alive(self) -> bool:
      """Returns whether the given animal is alive. See 'is_alive()' of parent 'Animal'."""
      return super().is_alive() and not self._killed
   
   def feed(self):
      """
      Feed method for Rabbit, increases its energy by eating grass.
      """
      if self.is_alive():
         can_eat = int(self._pop.metabolism * Rabbit.feeding_metabolism_rate) # int() to floor the value as grass should be an int
         if self._patch._grass - can_eat < 0: # Is there less grass than can be eaten in one step?
            food_amount = self._patch._grass
         else:
            food_amount = can_eat

         max_energy_addition = self._pop.max_energy - self.energy() 
         if max_energy_addition - food_amount < 0: # Are we eating more than we need to for max energy?
            food_amount = max_energy_addition # 1:1 grass-to-energy ratio
      
         self._patch._grass -= food_amount # int - int = int
         self._energy += food_amount # int + int = int

   def reproduce(self, newborn_patch: Patch) -> Optional[Rabbit]:
      """Reproduction method for the Rabbit class."""
      return super().reproduce(newborn_patch, Rabbit.reproduction_cost_rate)

   def same_species_in(self, patch: Patch) -> bool:
      """Checks if there are any rabbits in the given patch."""
      return patch.has_alive_rabbit()

   def predators_in(self, patch: Patch) -> bool:
      """Checks if there are any foxes in the given patch."""
      return patch.has_alive_fox()
