import matplotlib as matplot
import matplotlib.pyplot as plt
from results import *


def print_summary(results: SimulationStats):
   """Prints a short summary regarding the populations of the simulation."""

   for item in [['FOXES', results.foxes],['RABBITS', results.rabbits]]:
      animal = item[0]
      data = item[1]
      print(f"""
[{animal}]
Population
total: {data.total}
min: {min(data.size_per_step)}
avg: {sum(data.size_per_step)/len(data.size_per_step)}
max: {max(data.size_per_step)}

Deaths
total: {data.dead_by_old_age + data.dead_by_starvation + data.dead_by_predation}
old age: {data.dead_by_old_age}
starvation: {data.dead_by_starvation}
predation: {data.dead_by_predation}
""")


# Since we have to plot each population and their total,
# we will use for-loops with preset colors and styles
plt_style = ['--C1', '--C7', '-k']
plt_legend = ['Foxes','Rabbits','Total']


def _setup_plot(data, plot_title: str, x_label: str, y_label: str):
   """Generic function to set up the plot."""
   plt.title(plot_title)
   plt.xlabel(x_label)
   plt.ylabel(y_label)
   for i in range(len(data)):
      plt.plot(data[i], 
               plt_style[i],
               linewidth=1,
               scalex=True)
   plt.legend(plt_legend)


def plot_pop_size(results: SimulationStats):
   """Plots the size of the population for each step."""
   total_size_per_step = [results.foxes.size_per_step[i] + results.rabbits.size_per_step[i] for i in range(len(results.foxes.size_per_step))]
   plt_data = [results.foxes.size_per_step,
               results.rabbits.size_per_step,
               total_size_per_step]
   _setup_plot(plt_data, 'Population over time', 'Steps', 'Population size (living)')
   plt.show()
   

def plot_lifespan(results: SimulationStats):
   """Plots the lifespan of every individual that has ever lived during the simulation."""
   plt_data = [results.foxes.age_at_death, results.rabbits.age_at_death]
   _setup_plot(plt_data, 'Lifespans', 'Individuals', 'Age')
   plt.show()


def plot_energy(results: SimulationStats):
   """Plots the average energy of the animals per step."""
   plt_data = [results.foxes.avg_energy_per_step,
               results.rabbits.avg_energy_per_step,
               results.avg_energy_per_step]
   _setup_plot(plt_data, 'Average energy over time', 'Steps', 'Energy')
   plt.show()


def plot_kills(results: SimulationStats):
   """Plots kills on the grid."""
   max_kills = max([kill for patch in results.kills_per_patch for kill in patch])
   colormap = matplot.colors.LinearSegmentedColormap.from_list('kills',['white','yellow','orange','red'], 256)
   plt.imshow(results.kills_per_patch, cmap=colormap)
   plt.title('Distribution of kills by predators.')
   plt.colorbar(ticks=range(max_kills+1))
   plt.show()
   
