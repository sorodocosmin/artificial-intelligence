import math


class Functions:
    @staticmethod
    def relu(list_x):
        return list(map(lambda x: max(0, x), list_x))

    @staticmethod
    def relu_derivative(x):
        if x > 0:
            return 1
        else:
            return 0

    @staticmethod
    def sigmoid(list_x):
        return list(map(lambda x: 1 / (1 + math.exp(-x)), list_x))

    @staticmethod
    def sigmoid_derivative(x):
        return math.exp(-x) / ((1 + math.exp(-x)) ** 2)

    @staticmethod
    def softmax(list_x):
        """
        :param list_x: a list of numbers
        :return: a list of numbers, representing the percentages
        we will consider that won t have to deal with overflow
        """
        e_x = [math.exp(i) for i in list_x]
        sum_e_x = sum(e_x)
        return [i / sum_e_x for i in e_x]

    # @staticmethod
    # def softmax_derivative(list_softmax_output):
    #     """
    #     https://mmuratarat.github.io/2019-01-27/derivation-of-softmax-function#:~:text=Therefore%2C%20when%20we%20try%20to,of%20a%20vector%2Dvalued%20function.&text=In%20our%20case%2C%20gi,k%3D1exk.
    #     :param list_softmax_output:
    #     :return: a list of the derivatives of the softmax function
    #     """
    #     derivative_list = []
    #     for i in range(len(list_softmax_output)):
    #         pass

    # def softmax1_derivative(softmax_output):
    #     # Ensure softmax_output is a list
    #     softmax1_output = list(softmax_output)
    #
    #
    #     return derivative_vector

    @staticmethod
    def mean_squared_error(list_predicted, list_expected):
        """
        :param list_predicted: a list of numbers
        :param list_expected: a list of numbers
        :return: the mean squared error
        """
        if len(list_predicted) != len(list_expected):
            raise Exception("The lists should have the same length")

        return (sum([(list_predicted[i] - list_expected[i]) ** 2 for i in range(len(list_predicted))]) /
                (2 * len(list_predicted)))  # we use 2* to be able to derivate

    @staticmethod
    def cross_entropy(list_predicted, list_expected):
        epsilon = 1e-10

        # Limit predicted values to avoid log(0)
        clipped_predictions = [Functions.limit_value(value, epsilon, 1 - epsilon) for value in list_predicted]

        # Calculate cross-entropy
        cross_entropy = - sum(
            true_i * math.log(predicted_i) for true_i, predicted_i in zip(list_expected, clipped_predictions))

        return cross_entropy

    @staticmethod
    def limit_value(value, lower_bound, upper_bound):
        return max(lower_bound, min(value, upper_bound))
