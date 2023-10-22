import copy
from itertools import chain



class State:

    def __init__(self, instance_problem):
        """
        This is the function of initialisation (it gets the instance of the problem and forms the initial state)
        :param instance_problem:
        """
        self.matrix = (
            instance_problem[0:3],
            instance_problem[3:6],
            instance_problem[6:9]
        )
        self.last_cell_moved = None

    def __str__(self):
        """
        :return: a string that represents the instance of this class
        """
        return (f"[{self.matrix[0][0]}, {self.matrix[0][1]}, {self.matrix[0][2]}]\n"
                f"[{self.matrix[1][0]}, {self.matrix[1][1]}, {self.matrix[1][2]}]\n"
                f"[{self.matrix[2][0]}, {self.matrix[2][1]}, {self.matrix[2][2]}]"
                )

    def __eq__(self, other):
        """

        :param other:
        :return: true if the values from the matrix are in the same position
        """
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __hash__(self):

        return hash(self.matrix)

    def is_final(self):
        """
        Checks if the problem is in a final state by checking if all numbers are in ascendant order
        :return:
        """
        cell = self.matrix[0][0]
        for i in range(3):
            for j in range(3):
                if i == 0 and j == 0:
                    continue
                if self.matrix[i][j] < cell and self.matrix[i][j] != 0:
                    return False
                if self.matrix[i][j] != 0:
                    cell = self.matrix[i][j]

        return True

    def find_zero(self):
        """

        :return: a tuple (zero_line, zero_column)
        """
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == 0:
                    return i, j

    def transition_1(self):
        """
        Try to move the zero cell to the top
        :return:
        """
        z_i, z_j = self.find_zero()
        if self.transition_1_is_valid(z_i, z_j):
            # new_state = copy.deepcopy(self)
            matrix_list = [list(row) for row in self.matrix]
            matrix_list[z_i - 1][z_j], matrix_list[z_i][z_j] = matrix_list[z_i][z_j], matrix_list[z_i - 1][z_j]
            # swap the zero cell with the one above
            new_state = State(tuple(chain.from_iterable(matrix_list)))
            new_state.last_cell_moved = new_state.matrix[z_i][z_j]
            return new_state
        else:
            return None

    def transition_2(self):
        """
        Try to move the zero cell to the right
        :return:
        """
        z_i, z_j = self.find_zero()
        if self.transition_2_is_valid(z_i, z_j):
            # swap the zero cell with the one on the right
            matrix_list = [list(row) for row in self.matrix]
            matrix_list[z_i][z_j+1], matrix_list[z_i][z_j] = matrix_list[z_i][z_j], matrix_list[z_i][z_j+1]
            # swap the zero cell with the one above
            new_state = State(tuple(chain.from_iterable(matrix_list)))
            new_state.last_cell_moved = new_state.matrix[z_i][z_j]
            return new_state
        else:
            return None

    def transition_3(self):
        """
        Try to move the zero cell to the bottom
        :return:
        """
        z_i, z_j = self.find_zero()
        if self.transition_3_is_valid(z_i, z_j):
            matrix_list = [list(row) for row in self.matrix]
            matrix_list[z_i + 1][z_j], matrix_list[z_i][z_j] = matrix_list[z_i][z_j], matrix_list[z_i + 1][z_j]
            # swap the zero cell with the one above
            new_state = State(tuple(chain.from_iterable(matrix_list)))
            new_state.last_cell_moved = new_state.matrix[z_i][z_j]
            return new_state
        else:
            return None

    def transition_4(self):
        """
        Try to move the zero cell to the left
        :return:
        """
        z_i, z_j = self.find_zero()
        if self.transition_4_is_valid(z_i, z_j):
            # swap the zero cell with the one on the left
            matrix_list = [list(row) for row in self.matrix]
            matrix_list[z_i][z_j-1], matrix_list[z_i][z_j] = matrix_list[z_i][z_j], matrix_list[z_i][z_j-1]
            # swap the zero cell with the one above
            new_state = State(tuple(chain.from_iterable(matrix_list)))
            new_state.last_cell_moved = new_state.matrix[z_i][z_j]
            return new_state
        else:
            return None

    def transition_1_is_valid(self, i, j):
        """
        Check if you can move the zero cell above
        :param i:
        :param j:
        :return:
        """
        if i == 0:
            return False
        if self.matrix[i - 1][j] == self.last_cell_moved:
            return False

        return True

    def transition_2_is_valid(self, i, j):
        """
        Check if you can move the zero cell on the right
        :param i:
        :param j:
        :return:
        """
        if j == 2:
            return False
        if self.matrix[i][j + 1] == self.last_cell_moved:
            return False

        return True

    def transition_3_is_valid(self, i, j):
        """
        Check if you can move the zero cell on bottom
        :param i:
        :param j:
        :return:
        """
        if i == 2:
            return False
        if self.matrix[i + 1][j] == self.last_cell_moved:
            return False

        return True

    def transition_4_is_valid(self, i, j):
        """
        Check if you can move the zero cell on bottom
        :param i:
        :param j:
        :return:
        """
        if j == 0:
            return False
        if self.matrix[i][j - 1] == self.last_cell_moved:
            return False

        return True
