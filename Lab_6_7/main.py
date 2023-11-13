from data import Data
from NN import NeuralNetwork

data = Data('seeds/seeds_dataset.txt')
training_data, test_data = data.divide_in_training_and_test_data()

nn = NeuralNetwork(training_data)
nn.print_network()
nn.train()
# perceptron.test(test_data)

