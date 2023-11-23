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
    def sigmoid_derivative(list_x):
        return list(map(lambda x: 1/(1+math.exp(-x))*(1-1/(1+math.exp(-x))), list_x))

    @staticmethod
    def softmax(list_x):
        """
        :param list_x: a list of numbers
        :return: a list of numbers, representing the percentages
        we will consider that won t have to deal with overflow
        """
        # normalised form of softmax
        e_x = [math.exp(i) for i in list_x]
        sum_e_x = sum(e_x)
        return [i / sum_e_x for i in e_x]

    @staticmethod
    def softmax_derivative(x):
        return x*(1-x)

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
                (len(list_predicted)))

    @staticmethod
    def cross_entropy(list_predicted, list_expected):
        epsilon = 1e-10

        # Limit predicted values to avoid log(0)
        clipped_predictions = [Functions.limit_value(value, epsilon, 1 - epsilon) for value in list_predicted]
        clipped_expected = [Functions.limit_value(value, epsilon, 1 - epsilon) for value in list_expected]

        # Calculate cross-entropy
        cross_entropy = - sum(
            true_i * math.log(predicted_i) for true_i, predicted_i in zip(clipped_expected, clipped_predictions))

        return cross_entropy

    @staticmethod
    def limit_value(value, lower_bound, upper_bound):
        return max(lower_bound, min(value, upper_bound))

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
