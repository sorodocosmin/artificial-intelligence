import random

import numpy as np

from functions import Functions
from layer import Layer

"""
    There are many rule-of-thumb methods for determining the correct number of neurons to use in the hidden layers,
    such as the following:
- The number of hidden neurons should be between the size of the input layer and the size of the output layer.  (1)
- The number of hidden neurons should be 2/3 the size of the input layer, plus the size of the output layer.    (2)
- The number of hidden neurons should be less than twice the size of the input layer.                           (3)
We will be using the first one (1).
"""


class NeuralNetwork:
    def __init__(self, training_data, learning_rate=0.05, nr_epochs=500, nr_hidden_layers=2):
        self.__error_training = []
        self.__training_data = training_data
        self.__learning_rate = learning_rate
        self.__nr_epochs = nr_epochs
        self.__nr_hidden_layers = nr_hidden_layers

        self.__neurons_per_layer = [len(training_data[0]) - 1]
        self.__size_output_layer = len(set([row[-1] for row in training_data]))

        mini = min(self.__neurons_per_layer[0], self.__size_output_layer)
        maxi = max(self.__neurons_per_layer[0], self.__size_output_layer)

        for _ in range(self.__nr_hidden_layers):
            # we use the first rule, and choose a random nr between
            self.__neurons_per_layer.append(random.randint(mini, maxi))

        self.__neurons_per_layer.append(self.__size_output_layer)

        self.__layers = [Layer(self.__neurons_per_layer[0], 0, needs_weights=False)]

        for i in range(1, len(self.__neurons_per_layer)):
            self.__layers.append(Layer(self.__neurons_per_layer[i], self.__neurons_per_layer[i - 1]))

    def train(self, training_data):

        for epoch in range(self.__nr_epochs):
            error_epoch = 0
            random.shuffle(training_data)
            for inpt in training_data:
                label = inpt[-1]
                expected_output = [0] * self.__size_output_layer
                expected_output[int(label) - 1] = 1

                output = self.feed_forward(inpt[:-1])
                # print("Expected output: " + str(expected_output))
                # print("Output: " + str(output))
                error_epoch += Functions.mean_squared_error(expected_output, output)
                self.back_propagation(output, expected_output)

            print(f"epoch = {epoch} err={error_epoch/len(training_data)}")
            self.__error_training.append((epoch, error_epoch/len(training_data)))

    def feed_forward(self, input_data):
        output = []
        for i, layer in enumerate(self.__layers):
            if i == 0:
                layer.set_input(input_data)
            else:
                output = self.compute_output(input_data, layer)
                input_data = output

        return output

    def compute_output(self, input_data, layer):
        bias = layer.get_bias()
        result = bias + np.dot(input_data, layer.get_weights())
        layer.set_output(Functions.sigmoid(result))

        return Functions.sigmoid(result)

    def back_propagation(self, predicted_output, expected_output):
        gradients = []
        l_l_bias = self.__layers[-1].get_bias()
        previous_layer_output = self.__layers[-2].get_output()
        last_layer_gradients = (Functions.sigmoid_derivative(l_l_bias +
                                                             np.dot(previous_layer_output,
                                                                    self.__layers[-1].get_weights()))
                                * (np.array(expected_output) - predicted_output))
        gradients.append(last_layer_gradients)

        i = len(self.__layers) - 2

        while i > 0:
            l_bias = self.__layers[i].get_bias()

            previous_layer_output = self.__layers[i - 1].get_output()
            if i-1 == 0:
                previous_layer_output = self.__layers[i - 1].get_input()
            l_gradients = (Functions.sigmoid_derivative(l_bias +
                                                        np.dot(previous_layer_output, self.__layers[i].get_weights()))
                           * np.dot(np.array(gradients[-1]), np.array(self.__layers[i+1].get_weights()).T))
            gradients.append(l_gradients)
            i -= 1

        gradients.reverse()

        # update weights and bias
        for i, layer in enumerate(self.__layers):
            if i == 0:
                continue

            previous_layer_output = self.__layers[i - 1].get_output()
            if i == 1:
                previous_layer_output = self.__layers[i - 1].get_input()
            # compute delta/ corrections
            delta_w = self.__learning_rate * np.dot(np.array([previous_layer_output]).T, np.array(gradients[i - 1]).reshape(1, -1))
            layer.update_weights(delta_w)
            delta_b = self.__learning_rate * gradients[i - 1]
            layer.update_bias(delta_b)

    def test(self, test_data):
        """
        :param test_data: a list of instances
        :return: the accuracy of the network, correct_classified_points, incorrect_classified_points
        """
        nr_correct = 0
        correct_classified_points = []
        incorrect_classified_points = []
        for instance in test_data:
            print(f"Instance: {instance}")
            output = self.feed_forward(instance[:-1])
            print(f"Expected :{instance[-1]}")
            print(f"Predicted :{output}")
            predicted = output.index(max(output)) + 1
            print(f"Predicted class: {predicted}")

            if predicted == instance[-1]:
                nr_correct += 1
                correct_classified_points.append(instance)
            else:
                incorrect_classified_points.append(instance)

        return nr_correct / len(test_data), correct_classified_points, incorrect_classified_points

    def get_training_error(self):
        return self.__error_training

    def print_network(self):
        for i, layer in enumerate(self.__layers):
            print(f"Layer {i} - nr neurons = {layer.get_nr_neurons()}")
            print("Weights: ", layer.get_weights())
            print("Bias: ", layer.get_bias())
            print()
