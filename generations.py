import numpy as np
import random
from math import sin
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy



class Species:
    
    def __init__(self,weights=[]):
        self.fitness = 0
        self.brain = self.create_neuralnetowork(weights)

    def create_neuralnetowork(self,weights):
        if weights == []:
            model = Sequential([
            Dense(units=10, input_shape=(11,), activation="relu", bias_initializer="RandomNormal" ), #first hidden layer
            Dense(units=5, activation="softmax", bias_initializer="RandomNormal") #output
            ])
        else:
            model = Sequential([
            Dense(units=10, input_shape=(11,), activation="relu"), #first hidden layer
            Dense(units=5, activation="softmax") #output
            ])
            model.set_weights(weights)
        return model

    #@tf.function(input_signature=(tf.TensorSpec(shape=[1,11], dtype=tf.int32),))
    def spit_output(self, input_params:list):
        #print(f"input params:{input_params}")
        command_dict = {0:"eat", 1:"move_up", 2:"move_down", 3: "move_right", 4:"move_left"}
        #run neural net and convert input to command
        decisions = self.brain(np.array(input_params).reshape(1,11), training=False)
        #print(f"decisions: {decisions}")
        command_int = decisions.numpy().argmax()
        return command_dict[command_int]

    def set_fitness (self, fitness):
        self.fitness = fitness

class Generation:

    def __init__(self, gen_counter:int, top_performers:list):
        self.gen_counter = gen_counter
        self.neural_net_dict = self.create_generation(top_performers)
        
    def create_generation(self,top_performers:list):
        if self.gen_counter ==1:
            neural_net_dict = self.create_random_gens()
            return neural_net_dict
        else:
            neural_net_dict = self.create_fleming_gen(top_performers, random_gens=5)
            return neural_net_dict
    
    def create_random_gens(self):
        net_dict={}
        for x in range (0,10):
            net = Species()
            net_dict[x]=net
        return net_dict
    
    def get_mutated_weights(self, model, number_of_mutations=1):
        old_weights = model.weights
        old_shapes = []
        old_weights_flat = []
        new_weights = []

        for x in range(0,len(old_weights)):
            old_shapes.append(old_weights[x].numpy().shape)
            old_weights_flat.append(old_weights[x].numpy().flatten())
        
        #one big flat array
        weights_combined = np.concatenate(( old_weights_flat))

        #mutate
        for mut_num in range(0,number_of_mutations):
            random_num = random.randint(0, len(weights_combined)-1)
            mutation_value = sin(mut_num * random_num +random_num)
            weights_combined[random_num] = mutation_value


        #add new weights (and biases) to the list
        for x in range(0,len(old_weights)):
            new_weights.append(weights_combined[:len(old_weights_flat[x])].reshape(old_shapes[x]))
            weights_combined = np.delete(weights_combined,np.s_[:len(old_weights_flat[x])])

        return new_weights
    
    def create_fleming_gen(self,top_performer_weights, random_gens=5):
        net_dict={}
        fibbo = [34,21,13,8,5,3,2,1]
        
        fibbo_perf_dict = {fibbo[i]: top_performer_weights[i] for i in range(len(fibbo))}
        counter=0

        #instaed of hard coded 100 i should sum fibbo, random gens and len top perf
        while counter < 100:
            #create identical copies
            if counter <= 7:
                print(top_performer_weights[counter].weights)
                net = Species(weights=top_performer_weights[counter].weights)
                net_dict[counter] = net
                counter +=1
                print(net.brain)

            #create mutated versions of top performers 
            elif counter < 95:
                for key in fibbo_perf_dict: 
                    for x in range(0,key):
                        mutated_weights = self.get_mutated_weights(fibbo_perf_dict[key], number_of_mutations=x+1)
                        net = Species(weights=mutated_weights)
                        net_dict[counter] = net
                        counter +=1
                print(net.brain)

            #create randos
            else:
                net = Species(weights=[])
                net_dict[counter]=net
                counter +=1
                print(net.brain)
            
        return  net_dict

