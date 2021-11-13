import numpy as np
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
        model = Sequential([
        Dense(units=10, input_shape=(11,), activation="relu", bias_initializer="RandomNormal" ), #first hidden layer
        Dense(units=5, activation="softmax", bias_initializer="RandomNormal") #output
        ])
        return model

    #@tf.function(input_signature=(tf.TensorSpec(shape=[1,11], dtype=tf.int32),))
    def spit_output(self, input_params:list):
        command_dict = {0:"eat", 1:"move_up", 2:"move_down", 3: "move_right", 4:"move_left"}
        #run neural net and convert input to command
        decisions = self.brain(np.array(input_params).reshape(1,11), training=False)
        command_int = decisions.numpy().argmax()
        return command_dict[command_int]

    def set_fitness (self, fitness):
        self.fitness = fitness




class Generation:

    def __init__(self, gen_counter:int, top_performers:list):
        self.gen_counter = gen_counter
        self.neural_net_dict = self.create_generation(top_performers)
        

    def create_generation(self,top_performers:list):
        if self.gen_counter < 5:
            neural_net_dict = self.create_random_gens()
            return neural_net_dict
        else:
            neural_net_dict = {}#create_generation_according_to_rules(top_performers)
            return neural_net_dict
    
    def create_random_gens(self):
        net_dict={}
        for x in range (0,3):
            net = Species()
            net_dict[x]=net
        return net_dict
        
