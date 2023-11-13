import random


class Neuron:
    def __init__(self, nr_neurons_next_layer, needs_bias=True, needs_weights=True):
        """
        if needs_weights is False, then the nr_neurons_next_layer doesn't matter
        this type of neurons will be created on the output layer
        """

        # weights will be represented as a list
        # weights[i] = the weight of the connection between the current neuron and the i-th neuron from the next layer
        # bayes = ..
        # output = .. neurons from the input layer don't have an output,
        # or their output is the input of the instance from the training data
        self.__weights = []
        self.__bias = None
        self.__input_before_activation = None

        if needs_weights:
            for _ in range(nr_neurons_next_layer):
                w_i = random.uniform(-1, 1)
                while w_i == 0:
                    w_i = random.uniform(-1, 1)

                self.__weights.append(w_i)

        if needs_bias:
            pos_bias = random.uniform(-1, 1)
            while pos_bias == 0:
                pos_bias = random.uniform(-1, 1)

            self.__bias = pos_bias

    def get_weights(self):
        """
        :return: a list of wights with this specific:
        weight[i] = the w of the connection between this neuron and the i-th neuron from the next layer
        """
        return self.__weights

    def get_bias(self):
        return self.__bias

    def set_input_before_activation(self, output):
        self.__input_before_activation = output

    def get_input_before_activation(self):
        return self.__input_before_activation

    def update_weights(self, delta_w):
        for i in range(len(self.__weights)):
            self.__weights[i] += delta_w[i]

    def update_bias(self, delta_b):
        self.__bias += delta_b

    @staticmethod
    def multiply_matrix(matrix1, matrix2):
        """
        :param matrix1: a matrix
        :param matrix2: a matrix
        :return: the multiplication of the two matrices
        """

        # check if the matrices can be multiplied
        if len(matrix1[0]) != len(matrix2):
            raise Exception("The matrices cannot be multiplied")

        result = []
        for i in range(len(matrix1)):
            row = []
            for j in range(len(matrix2[0])):
                elem = 0
                for k in range(len(matrix2)):
                    elem += matrix1[i][k] * matrix2[k][j]
                row.append(elem)
            result.append(row)
        return result

    def __str__(self):
        return "Weights: " + str(self.__weights) + "\nBayes: " + str(self.__bias)
