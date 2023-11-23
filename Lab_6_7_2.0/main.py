import numpy as np

from data import Data
from NN import NeuralNetwork

import matplotlib.pyplot as plt


def visualize_errors(train_errors):
    plt.figure(figsize=(10, 5))

    nr_epochs, val_err = zip(*train_errors)
    plt.plot(nr_epochs, val_err, color='black')
    plt.title('Training Error')
    plt.xlabel('Epochs')
    plt.ylabel('MST')

    plt.show()


def visualize_points(incorrect_classified, correct_classified, accuracy):
    plt.figure(figsize=(10, 5))

    incorrect_classified = np.array(incorrect_classified)
    correct_classified = np.array(correct_classified)

    if len(incorrect_classified) > 0:
        plt.scatter(incorrect_classified[:, 0], incorrect_classified[:, 1], color='red', label='Incorrect Classified')

    if len(correct_classified) > 0:
        plt.scatter(correct_classified[:, 0], correct_classified[:, 1], label='Correct Classified')

    plt.title(f'Accuracy: {accuracy * 100:.2f}%')
    plt.xlabel('X-Label')
    plt.ylabel('Y-Label')
    plt.legend()
    plt.show()


def main():
    data = Data('seeds/seeds_dataset.txt')
    training_data, test_data = data.divide_in_training_and_test_data()

    print(training_data)

    nn = NeuralNetwork(training_data)
    nn.print_network()
    nn.train(training_data)
    accuracy, correct_classified, incorrect_classified = nn.test(test_data)
    visualize_errors(nn.get_training_error())
    visualize_points(incorrect_classified, correct_classified, accuracy)


if __name__ == '__main__':
    main()

