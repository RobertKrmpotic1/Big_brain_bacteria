# Big brain bacteria


## Summary
An evolutionary simulation using pygame and tensorflow.
An attempt to simulate simple evolving organisms by using custom evolutionary algorithm named Fibo-Fleming. The organisms need to evolve in an energy conistent system and outcompete others by eating and reproducing as fast as possible.

## How to run it
Prerequisites for running this project are pygame and tensorflow. Simply run main.py and watch the evolution unfold in front of your eyes.

## Simulation
The simulation is split into generations and rounds. Each generation has 100 spiecies which have a simple sequential neural network "brain". Each spiecies is tested for a round which is set on a 10x10 grid. The species are rated based on their fitness level which is measured by how much food they have eaten from the grid and max population size.

### The grid

The grid is a 10x10 tile grid. Each grid has 2 values which are visually mapped to the colour, amount of red and blue. The bacteria can interact with the grid by eating a certain colour from it and releasing colour into it. 

### The bacteria

The bacteria is a representation of a simple organism. It has only few attributes which are hunger, energy, speed, vision range, and affinity to eat red or blue. The hunger is just max energy - current energy. Once it reaches 90% energy it divides via mitosis and gives birth to another identical copy of itself. The energy is preserved during this process. The bacteria can "see" the colour of the tile it is standing on, as well as one tile around it in 4 directions. Bacteria has 5 possible actions each frame: move in a direction or eat.

### The brain
The actions of the bacteria are decided by sequential neural network. It has several inputs which are colours of the tile around it as well as the tile it is currently standing on. It also receives its current hunger as input. The output of the neural network is mapped to 5 possible actions: move in a direction or eat. The brains among species differ in weights and biases of neurons in the neural network.

### Rounds
In each round only a single species particiapte on a grid. It has a time limit and needs to eat as much food off the tiles as possible and produce as many copies of itself. 

### Generations
Each generation has 100 species and each gets to be tested in a round. All species of a generation are tested on the same grid. The grid changes each generation and is randomly generated. The first generation is randomly generated. The other generations are generated using custom evolutionary algorithm called Fibbo-Fleming which allows top 8 species to mutate and create offspring, rewarding the best performing species with the most offspring. 

### Fibo-Fleming algorithm

This algorithm is made to reward the highest performering neural network with most offspring with varying degrees of mutations. 
In this example 100 species need to be produced from top 8 performers. Each of them gets one exact replica in the next generation. Moreover, the 8th performer (last in the top list) gets 1 additional copy with 1 modified weight or bias. The 7th gets 2 additional copies with first one having 1 modification and second one having 2... and so on following Fibonacci sequence. Finally, the top performer will have 34 mutant copies with most mutated one having 34 modifications to the weights and bias of the neural network. 

Therefore, the new generation will consist of: 8 exact replicas of top performers,  87 mutants, and 5 nets where the weights and biases are completely randomised. 
