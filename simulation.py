import random
import entities
import visualiser as vis
import parameters
import results
from typing import Union, List, Tuple


    

def run(parameters):
    patches = []
    sim_step = 0
    all_dead = False
    stats = results.SimulationStats()

    for x in range(parameters.world.west_east_length):
        stats.kills_per_patch.append([])
        for y in range(parameters.world.north_south_length):
            stats.kills_per_patch[x].append(0)
    
    for i in range(parameters.world.area()):
        patches.append(entities.Patch(i % parameters.world.west_east_length, i // parameters.world.west_east_length))

    def data_on_birth(animal):
        """Records every number of living members of each species upon birth."""
        if type(animal) is entities.Fox:
            stats.foxes.total += 1
        else:
            stats.rabbits.total += 1
        

    def init_animals(animal_entity: type(entities.Animal), pop_parameters: type(parameters.rabbits)):
        """"Adds the initial population to random patches of grass in the world."""
        counter = 0
        while counter < pop_parameters.initial_size:
            index = random.randint(0, len(patches) - 1) # Choose a random patch
            
            if len(patches[index].animals()) == 0 or len(patches[index].animals()) == 1 and type(patches[index].animals()[0]) is not animal_entity:
                # If the patch is empty, or if there is another animal but it isn't of the same type, add the animal.
                patches[index].add(animal_entity(pop_parameters, patches[index], random.randint(0, pop_parameters.max_age)))
                data_on_birth(animal_entity)
                counter += 1


    def data_on_death(animal):
        """Updates results class with data upon death of animal entities."""
        if type(animal) == entities.Fox:
            popStats = stats.foxes
        else:
            popStats = stats.rabbits

        popStats.age_at_death.append(animal.age)

        ### CAUSE OF DEATH
        if animal.energy() <= 0: # Not enough food; mainly an issue for wolves.
                popStats.dead_by_starvation += 1
        elif type(animal) == entities.Rabbit and animal.was_killed(): # Only occurs for rabbits
            popStats.dead_by_predation += 1
            coords = animal.patch().coordinates()
            stats.kills_per_patch[coords[0]][coords[1]] += 1
            
        else: # Since we cannot get the species parameters from the animal and this is the last possible scenario, else.
            popStats.dead_by_old_age += 1
        


    def get_legal_move(current_patch: type(entities.Patch), moving_animal: type(entities.Animal), is_reproducing: bool = False) -> Union[entities.Patch, None]:
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
                    
        else: # If not toroid
            for i in range(len(all_moves)):
                if all_moves[i][0] < 0 or all_moves[i][1] < 0 or all_moves[i][0] >= parameters.world.west_east_length or all_moves[i][0] >= parameters.world.north_south_length:
                    all_moves.pop(i) # Remove all illegal moves, i.e. points whose coordinates are out of range.


        index_from_coords = lambda x,y: x + parameters.world.west_east_length * y #Gets index from x and y value

        for i in all_moves:
            legal_moves.append(i)
            
        for coordinate_index in range(len(all_moves)):
            potential_patch = patches[index_from_coords(*all_moves[coordinate_index])]
            
            if moving_animal.same_species_in(potential_patch):
                legal_moves.remove(all_moves[coordinate_index]) # Remove all patches with same species in it
            elif moving_animal.predators_in(potential_patch) and is_reproducing:
                legal_moves.remove(all_moves[coordinate_index]) # Remove all predator patches if reproducing

        if legal_moves == []:
            move = None
        else:
            move = patches[index_from_coords(*random.choice(legal_moves))]
        
        return move


    init_animals(entities.Rabbit, parameters.rabbits)
    init_animals(entities.Fox, parameters.foxes)

    world = vis.ColourGraphics(parameters.execution.max_steps, patches, parameters.world.west_east_length, parameters.world.north_south_length)
    world.start()

    while sim_step < parameters.execution.max_steps and not all_dead:
        all_dead = True
        
        for patch in patches:
            patch.tick()
            if len(patch.animals()) > 0:
                for animal in patch.animals():
                    if animal.is_alive():
                        all_dead = False
                        animal.tick()

                        if animal.predators_in(animal.patch()):
                            animal.kill() #Kill bunny if starting turn on fox square
                        else:
                            animal.feed() #Otherwise eat

                        if not animal.is_alive(): #If dead
                            data_on_death(animal)
    
                        
                        if animal.can_reproduce():
                            baby_patch = get_legal_move(animal.patch(), animal, True)
                            if baby_patch is not None:
                                animal.reproduce(baby_patch)
                                data_on_birth(animal) # Note that we can pass animal as we only need its type
                                
                        elif animal.is_alive():
                            new_patch = get_legal_move(animal.patch(), animal)
                            if new_patch is not None:
                                animal.move_to(new_patch)

        sim_step += 1
        world.update(i)
        
    world.close()
    return stats
