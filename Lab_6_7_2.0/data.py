import re
import random


class Data:
    def __init__(self, path):
        """
        reads tje data from file and stores it in a matrix
        :param path:
        """
        self.__data = []

        with open(path, 'r') as file:
            for line in file:
                # split the line using spaces or tabs (with regex)
                values = re.split(r'\s+', line.strip())

                floats = [self.parse_float(value) for value in values]
                self.__data.append(floats)

    def get_data(self):
        return self.__data

    def divide_in_training_and_test_data(self):
        """
        it will split randomly the data in 80% of training data and 20% of test data
        :return: a tuple of two matrices: (training_data, test_data)
        """
        nr_of_rows = len(self.__data)

        data_class_1 = [item for item in self.__data if item[-1] == 1]
        data_class_2 = [item for item in self.__data if item[-1] == 2]
        data_class_3 = [item for item in self.__data if item[-1] == 3]

        rows_added_to_training_data = set()

        training_data = []

        rand_row_c_1 = random.randint(0, len(data_class_1) - 1)
        rand_row_c_2 = random.randint(0, len(data_class_2) - 1)
        rand_row_c_3 = random.randint(0, len(data_class_3) - 1)

        # we make sure that we have at least one row for each class in the training data
        training_data.append(data_class_1[rand_row_c_1])
        training_data.append(data_class_2[rand_row_c_2])
        training_data.append(data_class_3[rand_row_c_3])

        rows_added_to_training_data.add(rand_row_c_1)
        rows_added_to_training_data.add(rand_row_c_2)
        rows_added_to_training_data.add(rand_row_c_3)

        nr_of_rows_training_data = nr_of_rows * 0.8
        current_nr_rows = 3

        while current_nr_rows < nr_of_rows_training_data:
            rand_row = random.randint(0, nr_of_rows - 1)
            if rand_row not in rows_added_to_training_data:
                training_data.append(self.__data[rand_row])
                rows_added_to_training_data.add(rand_row)
                current_nr_rows += 1

        test_data = []
        # rows that are not in the training data will be added to the test data
        for i, row in enumerate(self.__data):
            if i not in rows_added_to_training_data:
                test_data.append(row)

        return training_data, test_data

    @staticmethod
    def parse_float(value):
        try:
            return float(value)
        except ValueError:
            # If it's not a valid float, return None
            return None
