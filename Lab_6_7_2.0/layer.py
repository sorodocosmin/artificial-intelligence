import random


class Layer:
    def __init__(self, nr_neurons, nr_neurons_previous_layer, needs_weights=True):
        """
        :param nr_neurons: the number of neurons in the current layer
        :param nr_neurons_previous_layer: the number of neurons in the previous layer
        :param needs_bias: if the neurons in this layer need a bias
        :param needs_weights: if the neurons in this layer need weights
        """
        self.__weights = []  # it will be a matrix
        self.__bias = []
        self.__output = []

        self.__nr_neurons = nr_neurons
        self.__weights = []

        if needs_weights:
            for _ in range(nr_neurons_previous_layer):
                list_w = []
                for _ in range(nr_neurons):
                    w_i = random.uniform(-1, 1)
                    while w_i == 0:
                        w_i = random.uniform(-1, 1)
                    list_w.append(w_i)
                self.__weights.append(list_w)

            for _ in range(nr_neurons):
                pos_bias = random.uniform(-1, 1)
                while pos_bias == 0:
                    pos_bias = random.uniform(-1, 1)
                self.__bias.append(pos_bias)
        else:
            self.__input = None

    def update_weights(self, delta_w):
        for i in range(len(self.__weights)):
            for j in range(len(self.__weights[i])):
                self.__weights[i][j] += delta_w[i][j]

    def update_bias(self, delta_b):
        for i in range(len(self.__bias)):
            self.__bias[i] += delta_b[i]

    def set_input(self, input_list):
        """
        Only for the first layer it will be used
        :param input_list:
        """
        self.__input = input_list

    def set_output(self, output_list):
        self.__output = output_list

    def get_input(self):
        return self.__input

    def get_output(self):
        return self.__output

    def get_weights(self):
        return self.__weights

    def get_bias(self):
        return self.__bias

    def get_nr_neurons(self):
        return self.__nr_neurons

