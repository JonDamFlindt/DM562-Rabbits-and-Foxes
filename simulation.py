import random
import entities
import visualiser as vis
import parameters as pars
import results
from typing import Union, List, Tuple


def run(parameters: pars.Simulation) -> results.SimulationStats:
    """Runs the simulation given the given parameters and returns a SimulationStats object."""
    patches = []
    sim_step = 0
    all_dead = False
    moved_this_turn = [] # Used to make the animals only move once
    stats = results.SimulationStats()

    for x in range(parameters.world.west_east_length):
        stats.kills_per_patch.append([])
        for y in range(parameters.world.north_south_length):
            stats.kills_per_patch[x].append(0)
            patches.append(entities.Patch(x,y))

    def data_on_birth(animal):
        """Records every number of living members of each species upon birth."""
        if isinstance(animal, entities.Fox):
            stats.foxes.total += 1
        else:
            stats.rabbits.total += 1
        

    def init_animals(animal_entity: entities.Animal, pop_parameters: pars.Population):
        """"Adds the initial population to random patches of grass in the world."""
        counter = 0
        while counter < pop_parameters.initial_size:
            index = random.randint(0, len(patches) - 1) # Choose a random patch
            
            if len(patches[index].animals()) <= 1 and isinstance(patches[index].animals()[0], animal_entity):
                # If the patch is empty, or if there is another animal but it isn't of the same type, add the animal.
                animal_entity(pop_parameters, patches[index], random.randint(0, pop_parameters.max_age))
                data_on_birth(animal_entity)
                counter += 1


    def data_on_death(animal):
        """Updates results class with data upon death of animal entities."""
        if isinstance(animal, entities.Fox):
            popStats = stats.foxes
        else:
            popStats = stats.rabbits

        popStats.age_at_death.append(animal.age())

        ### CAUSE OF DEATH
        if animal.energy() <= 0: # Not enough food; mainly an issue for wolves.
                popStats.dead_by_starvation += 1
        elif isinstance(animal, entities.Rabbit) and animal.was_killed(): # Only occurs for rabbits
            popStats.dead_by_predation += 1
            coords = animal.patch().coordinates()
            stats.kills_per_patch[coords[0]][coords[1]] += 1
            
        else: # Since we cannot get the species parameters from the animal and this is the last possible scenario, else.
            popStats.dead_by_old_age += 1
        


    def get_legal_move(current_patch: entities.Patch, moving_animal: entities.Animal, is_reproducing: bool = False) -> Union[entities.Patch, None]:
        """Checks if surrounding tiles are valid for movement and/or reproduction."""
        all_moves = []
        legal_moves = []
        coords = list(current_patch.coordinates())
        
        all_moves.append([coords[0], coords[1] - 1]) # Up
        all_moves.append([coords[0], coords[1] + 1]) # Down
        all_moves.append([coords[0] - 1, coords[1]]) # Left
        all_moves.append([coords[0] + 1, coords[1]]) # Right
            

        if parameters.world.is_toroid: # If toroid, make coordinates "loop".
            for i in range(len(all_moves)): #Re-index all points to the visible plane/within range
                all_moves[i][0]  %= parameters.world.west_east_length
                all_moves[i][1] %= parameters.world.north_south_length
                legal_moves.append(all_moves[i])
                    
        else: # If not toroid
            for i in range(len(all_moves)):
                if all_moves[i][0] >= 0 and all_moves[i][1] >= 0 and all_moves[i][0] < parameters.world.west_east_length and all_moves[i][1] < parameters.world.north_south_length:
                    legal_moves.append(all_moves[i]) # Remove all illegal moves, i.e. points whose coordinates are out of range.
            all_moves = [move for move in all_moves if move in legal_moves]
            

        def index_from_coords(x: int, y: int) -> int:
            """Gets the index from a patch's coordinates."""
            return x + parameters.world.west_east_length * y
        
        for i in range(len(all_moves)):
            potential_patch = patches[index_from_coords(*all_moves[i])]
            
            if moving_animal.same_species_in(potential_patch):
                legal_moves.remove(all_moves[i]) # Remove all patches with same species in it
            elif moving_animal.predators_in(potential_patch) and is_reproducing:
                legal_moves.remove(all_moves[i]) # Remove all predator patches if reproducing

        if legal_moves == []:
            move = None
        else:
            move = patches[index_from_coords(*random.sample(legal_moves,1))]
            moved_this_turn.append(moving_animal)
        
        return move


    init_animals(entities.Rabbit, parameters.rabbits) # Add rabbit population
    init_animals(entities.Fox, parameters.foxes) # Add fox population


    #Visuals/no visuals
    if parameters.execution.batch:
        world = vis.Batch(parameters.execution.max_steps)
    else:
        world = vis.ColourGraphics(parameters.execution.max_steps, patches, parameters.world.west_east_length, parameters.world.north_south_length)
    world.start()
    
    ### SIMULATION
    while sim_step < parameters.execution.max_steps and not all_dead:
        # Initializing variables per step of simulation
        stats.avg_energy_per_step.append(0)
        stats.rabbits.avg_energy_per_step.append(0)
        stats.foxes.avg_energy_per_step.append(0)
        stats.rabbits.size_per_step.append(0)
        stats.foxes.size_per_step.append(0)
        alive_foxes = 0
        alive_rabbits = 0
        all_dead = True # Used to stop the simulation if all animals die
        moved_this_turn = [] # Used to make the animals only move once
        
        for patch in patches: # For every patch
            patch.tick() # Grass grows
            if len(patch.animals()) > 0:
                for animal in patch.animals():
                    if animal.is_alive() and animal not in moved_this_turn:
                        all_dead = False # At least one
                        animal.tick() # Animal ages/starves


                        if len(animal.patch().animals()) == 2 and animal.is_alive(): # If rabbit and fox on square
                          for entity in animal.patch().animals():
                            if isinstance(animal, entities.Fox) and isinstance(entity, entities.Rabbit) and entity.is_alive():
                              animal.feed()
                              entity.kill()
                              data_on_death(entity)
                            elif isinstance(animal, entities.Rabbit) and isinstance(entity, entities.Fox) and animal.is_alive():
                              entity.feed()
                              animal.kill()
                              data_on_death(animal)
                        elif isinstance(animal, entities.Rabbit):
                            animal.feed() #Otherwise rabbits eat

                        elif not animal.is_alive(): #If dead, update death data
                            data_on_death(animal)
    
                        new_patch = get_legal_move(animal.patch(), animal) # For movement in case reproduction does not occur
                        if animal.can_reproduce():
                            baby_patch = get_legal_move(animal.patch(), animal, True)
                            if baby_patch is not None:
                                baby = animal.reproduce(baby_patch)
                                if baby is not None:
                                    data_on_birth(baby)
                            elif new_patch is not None:
                                animal.move_to(new_patch)
                                
                                
                        elif animal.is_alive(): #Only if the animal is alive and cannot reproduce
                            if new_patch is not None:
                                animal.move_to(new_patch)

                            if isinstance(animal, entities.Fox):
                                stats.foxes.size_per_step[sim_step] += 1
                                stats.foxes.avg_energy_per_step[sim_step] += animal.energy()
                                alive_foxes += 1
                            elif isinstance(animal, entities.Rabbit):
                                stats.rabbits.size_per_step[sim_step] += 1
                                stats.rabbits.avg_energy_per_step[sim_step] += animal.energy()
                                alive_rabbits += 1

            
        if alive_foxes > 0 or alive_rabbits > 0:
            stats.avg_energy_per_step[sim_step] = (stats.foxes.avg_energy_per_step[sim_step] + stats.rabbits.avg_energy_per_step[sim_step]) / (alive_foxes + alive_rabbits)
            if alive_foxes > 0:
                stats.foxes.avg_energy_per_step[sim_step] /= alive_foxes
            if alive_rabbits > 0:
                stats.rabbits.avg_energy_per_step[sim_step] /= alive_rabbits
        
        world.update(sim_step)
        sim_step += 1
        
    world.stop()
    return stats
