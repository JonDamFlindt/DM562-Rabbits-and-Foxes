import random
import entities
import visualiser as vis
import parameters
import results
from typing import Union, List, Tuple


    

def run(parameters):
    patches = []
    stats = results.SimulationStats()
    
    for i in range(parameters.world.area()):
        patches.append(entities.Patch(i % parameters.world.west_east_length, i // parameters.world.west_east_length))

    def data_on_birth(animal):
        """Records every living member of each species upon birth."""
        if type(animal) is entities.Fox:
            stats.foxes.total += 1
        else:
            stats.rabbits.total += 1
        

    def init_animals(animal: entities.Animal, pop_parameters: Union[parameters.rabbits, parameters,foxes]):
        """"Adds the initial population to random patches of grass in the world."""
        counter = 0
        while counter < pop_parameters.initial_size:
            index = random.randint(0, len(patches) - 1) # Choose a random patch
            
            if len(patches[index].animals()) == 0 or len(patches[index].animals()) == 1 and type(patches[index].animals()[0]) is not animal_entity:
                # If the patch is empty, or if there is another animal but it isn't of the same type, add the animal.
                patches[index].add(animal(pop_parameters, patches[index], random.randint(0, pop_parameters.max_age)))
                data_on_birth(animal)
                counter += 1


    def data_on_death(animal):
        """Updates results class with data upon death of animal entities."""
        if type(animal) == entities.Fox:
            popStats = stats.foxes
        else:
            popStats = stats.rabbits

        popStats.age_at_death.append(animal.age)

        ### CAUSE OF DEATH
        if animal.energy <= 0: # Not enough food; mainly an issue for wolves.
                popStats.dead_by_starvation += 1
        elif animal.was_killed(): # Only occurs for rabbits
            stats.dead_by_predation += 1
            coords = animal.patch().coordinates()
            stats.kills_per_patch[coords[0][coords[1]]] += 1
            
        else: # Since we cannot get the species parameters from the animal and this is the last possible scenario, else.
            popStats.dead_by_old_age += 1
        


    def get_legal_move(current_patch: entities.Patch, moving_animal: entities.Animal, is_reproducing: bool = False) -> Union[entities.Patch, None]:
        """Checks if surrounding tiles are valid for movement and/or reproduction."""
        legal_moves = []
        coords = list(current_patch.coordinates())
        
        legal_moves.append([coords[0], coords[1] + 1]) # Up
        legal_moves.append([coords[0], coords[1] - 1]) # Down
        legal_moves.append([coords[0] - 1, coords[1]]) # Left
        legal_moves.append([coords[0] + 1, coords[1]]) # Right


        if parameters.world.is_toroid: # If toroid, make coordinates "loop".
            for i in range(legal_moves): #Re-index all points to the visible plane/within range
                legal_moves[i][0]  %= parameters.world.west_east_length
                legal_moves[i][1] //= parameters.world.west_east_length
                    
        else: # If not toroid
            for i in range(legal_moves):
                if legal_moves[i][0] < 0 or coords[1] < 0 or coords[0] > parameters.world.west_east_length - 1 or coords[0] > parameters.world.north_south_length - 1:
                    legal_moves.pop(i) # Remove all illegal moves, i.e. points whose coordinates are out of range.


        index_from_coords = lambda x,y: x + parameters.world.west_east_length * y #Gets index from x and y value

        for new_coords in legal_moves:
            potential_patch = patches[index_from_coords(*new_coords)] 
            patch_animals = potential_patch.animals()
            if len(patch_animals) == 2 or len(patch_animals) == 1 and moving_animal.same_species_in(potential_patch):
                legal_moves.pop(coords) # Remove all full patches
            if len(patch_animals) == 1 and moving_animal.predators_in(potential_patch) and is_reproducing:
                legal_moves.pop(coords) # Remove all predator patches if reproducing

        if legal_moves == []:
            move = None
        else:
            move = patches(index_from_coords(*random.choice(legal_moves)))

        return move


    init_animals(entities.Rabbit, parameters.rabbits)
    init_animals(entities.Fox, parameters.foxes)

    world = vis.ColourGraphics(parameters.execution.max_steps, patches, parameters.world.west_east_length, parameters.world.north_south_length)
    world.start()    
    for i in range(parameters.execution.max_steps):
        for patch in patches:
            patch.tick()
            
            if len(patch.animals()) > 0:
                for animal_index in range(len(patch.animals())):
                    animal = patch.animals()[animal_index]
                    animal.tick()

                    if len(animal.patch().animals()) == 2 and type(animal.patch().animals()[0]) is entities.Rabbit: 
                        animal.kill() #Kill bunny if starting turn on fox square
                    else:
                        animal.feed() #Otherwise eat

                    if not animal.is_alive(): #If dead
                        data_on_death(animal)
                        animal.patch().remove(animal)
                        
                    if animal.can_reproduce():
                        baby_patch = get_legal_move(animal.patch())
                        if baby_patch is not None:
                            animal.reproduce(baby_patch)
                            data_on_birth(animal) # Note that we can pass animal as we only need its type
                    
                            
    

        world.update(i)

    world.close()
