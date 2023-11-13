import random
from neuron import Neuron
from functions import Functions

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
        self.__training_data = training_data
        self.__learning_rate = learning_rate
        self.__nr_epochs = nr_epochs

        self.__size_start_layer = len(training_data[0]) - 1

        # go from all the train_dta and check how many dif classes we have
        self.__size_output_layer = len(set([row[-1] for row in training_data]))

        self.__nr_hidden_layers = nr_hidden_layers
        self.__nr_neurons_hidden_layer = []

        mini = min(self.__size_start_layer, self.__size_output_layer)
        maxi = max(self.__size_start_layer, self.__size_output_layer)

        for _ in range(self.__nr_hidden_layers):
            # we use the first rule, and choose a random nr between
            self.__nr_neurons_hidden_layer.append(random.randint(mini, maxi))

        nr_total_layers = 1 + self.__nr_hidden_layers + 1
        self.__network = []
        for i in range(nr_total_layers - 1):
            list_neurons = []

            needs_bias = True

            if i != nr_total_layers - 2:
                if i == 0:
                    needs_bias = False
                for _ in range(self.__size_start_layer):
                    neuron = Neuron(self.__nr_neurons_hidden_layer[i], needs_bias=needs_bias)
                    list_neurons.append(neuron)
            else:  # last hidden layer
                for _ in range(self.__size_start_layer):
                    neuron = Neuron(self.__size_output_layer, needs_bias=needs_bias)
                    list_neurons.append(neuron)

            self.__network.append(list_neurons)

        # output layer
        list_neurons = []
        for _ in range(self.__size_output_layer):
            neuron = Neuron(0, needs_weights=False)
            list_neurons.append(neuron)

        self.__network.append(list_neurons)

    def train(self):
        # feed forward only the first instance

        input_dta = self.__training_data[0]
        label = input_dta[-1]
        expected_output = [0 for _ in range(self.__size_output_layer)]
        expected_output[int(label) - 1] = 1

        # Feed forward
        output = self.feed_forward(input_dta[:-1])

        print("Expected output: " + str(expected_output))
        print("Output: " + str(output))
        # Cross Entropy is good for when we have softmax on last layer
        error_cc = Functions.cross_entropy(output, expected_output)
        error_mse = Functions.mean_squared_error(output, expected_output)
        print(f"Error mse: {error_mse}")
        print(f"Error Cross Entropy: {error_cc}")
        self.back_propagation(expected_output, output)

        # print("Training started")
        # for _ in range(self.__nr_epochs):
        #     random.shuffle(self.__training_data)
        #     for input_dta in self.__training_data:
        #
        #         label = input_dta[-1]
        #         expected_output = [0 for _ in range(self.__size_output_layer)]
        #         expected_output[int(label) - 1] = 1
        #
        #         # Feed forward
        #         output = self.feed_forward(input_dta[:-1])
        #
        #         # print("Expected output: " + str(expected_output))
        #         # print("Output: " + str(output))
        #         # Cross Entropy is good for when we have softmax on last layer
        #         # error = Functions.cross_entropy(output, expected_output)
        #         error = Functions.mean_squared_error(output, expected_output)
        #         print(f"Error: {error}")
        #         self.back_propagation(expected_output, output)
        # print("Training finished")

    def feed_forward(self, input_data):
        nr_layers = len(self.__network)
        # for the first layer, we will set the input, as the input of the instance
        for i, neuron_start_layer in enumerate(self.__network[0]):
            neuron_start_layer.set_input_before_activation(input_data[i])

        for i in range(nr_layers - 2):
            output = self._compute_output(input_data, self.__network[i], self.__network[i + 1], Functions.relu)
            input_data = output

        # for the last layer, we will use softmax -- not yet, because idk it s derivative
        # output = self._compute_output(input_data, self.__network[-2], self.__network[-1], Functions.softmax)
        output = self._compute_output(input_data, self.__network[-2], self.__network[-1], Functions.softmax)
        return output

    def back_propagation(self, expected, predicted):
        e = []
        for i in range(len(expected)):
            e.append(expected[i] - predicted[i])

        gradient = []  # it will be a matrix, where line 0 represents last_layer
        last_layer_grad = []
        for i, neuron in enumerate(self.__network[-1]):
            last_layer_grad.append(e[i] *
                                   Functions.relu_derivative(neuron.get_input_before_activation()))
        gradient.append(last_layer_grad)

        i = len(self.__network) - 2

        while i >= 0:
            layer_grad = []
            for j, neuron in enumerate(self.__network[i]):
                s = 0
                for k, weight in enumerate(neuron.get_weights()):
                    s += gradient[-1][k] * weight
                layer_grad.append(s * Functions.relu_derivative(neuron.get_input_before_activation()))
            gradient.append(layer_grad)
            i -= 1

        gradient.reverse()

        # corections of biases and weights

        weights_delta = []
        bias_delta = []

        for i, layer in enumerate(self.__network[:-1]):  # we don t need to compute for the last layer
            layer_delta_w = []
            layer_delta_b = []
            for j, neuron in enumerate(layer):
                delta_w = []
                nr_wights = len(neuron.get_weights())
                for _ in range(nr_wights):
                    if i != 0:
                        delta_w.append(self.__learning_rate * gradient[i][j] *
                                       neuron.get_input_before_activation())
                    else:
                        delta_w.append(self.__learning_rate * gradient[i][j] *
                                       Functions.relu([neuron.get_input_before_activation()])[0])
                        # functions relu takes a list, so we form one, then from what returns, we take the first element

                layer_delta_w.append(delta_w)

            weights_delta.append(layer_delta_w)

            for j, neuron in enumerate(self.__network[i+1]):  # biases from next layer
                layer_delta_b.append(self.__learning_rate*gradient[i+1][j])

            bias_delta.append(layer_delta_b)

        # update weights and biases
        self.update_weights_and_biases(weights_delta, bias_delta)

    def update_weights_and_biases(self, weights_delta, bias_delta):
        for i, layer in enumerate(self.__network):
            for j, neuron in enumerate(layer):
                if i != len(self.__network)-1:
                    neuron.update_weights(weights_delta[i][j])
                if i != 0:
                    neuron.update_bias(bias_delta[i-1][j])

    def test(self, test_data):
        """
        :param test_data: a list of instances
        :return: the accuracy of the network
        """
        nr_correct = 0
        for instance in test_data:
            output = self.feed_forward(instance[:-1])
            print(f"Expected :{instance[-1]}")
            print(f"Predicted :{output}")
            predicted = output.index(max(output)) + 1
            if predicted == instance[-1]:
                nr_correct += 1

        print(f"Accuracy: {nr_correct} / {len(test_data)}")



    @staticmethod
    def _compute_output(input_data, layer1, layer2, activation_function):
        output = [neuron.get_bias() for neuron in layer2]

        for i, neuron in enumerate(layer1):
            weights = neuron.get_weights()
            for j, weight in enumerate(weights):
                output[j] += weight * input_data[i]

        for i, neuron in enumerate(layer2):
            neuron.set_input_before_activation(output[i])

        return activation_function(output)

    def print_network(self):
        print("Input layer: " + str(self.__size_start_layer))
        print("Hidden layers: " + str(self.__nr_hidden_layers))
        print("Neurons in hidden layers: " + str(self.__nr_neurons_hidden_layer))
        print("Output layer: " + str(self.__size_output_layer))
        for i, layer in enumerate(self.__network):
            print("Layer " + str(i) + ":")
            for neuron in layer:
                print(neuron)
            print()
