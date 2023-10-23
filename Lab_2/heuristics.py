from state import State


def find_number_in_matrix(matrix, nr) -> ():
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == nr:
                return i, j

    return None


def manhattan_heuristic(matrix) -> float:
    """
    To measure closeness between a current state and all the final states we can add up/ average all heuristic scores
    measuring the closeness between that current state and each final state.
    The manhattan distance is defined as : sum (from i to n) |x_i - y_i| (for n-dimensional points) ----- |x_1 - x_2| + |y_1 - y_2| (2 dimensional points)
    :param matrix:
    :return:
    """
    list_possible_final_states = State.possible_final_states()
    nr_final_states = len(list_possible_final_states)
    sum_distance = 0
    for state in list_possible_final_states:
        for i in range(3):
            for j in range(3):
                i_should_be, j_should_be = find_number_in_matrix(state, matrix[i][j])
                manh_dist = abs(i-i_should_be) + abs(j-j_should_be)
                sum_distance += manh_dist

    sum_distance /= nr_final_states

    return sum_distance


def hamming_heuristic(matrix) -> float:
    """
    it measures the minimum number of substitutions required to change one string into the other.
    Ex :    "karolin" and "kerstin" is 3.
            1011101 and 1001001 is 2.
    :param matrix:
    :return:
    """
    list_possible_final_states = State.possible_final_states()
    sum_dif = 0
    for state in list_possible_final_states:
        nr_dif = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != matrix[i][j]:
                    nr_dif += 1
        sum_dif += nr_dif

    sum_dif /= len(list_possible_final_states)

    return sum_dif


def chebyshev_heuristic(matrix) -> float:
    """
    The distance between 2 points A(x1,y2,z1) and B(x2,y2,z2) is calculated as:
        d = max(|x1-x2|, |y1-y2|, |z2-z2|)
    :param matrix:
    :return:
    """
    list_possible_final_states = State.possible_final_states()
    nr_final_states = len(list_possible_final_states)
    sum_distance = 0
    for state in list_possible_final_states:
        for i in range(3):
            for j in range(3):
                i_should_be, j_should_be = find_number_in_matrix(state, matrix[i][j])
                cheby_dist = max(abs(i-i_should_be), abs(j-j_should_be))
                sum_distance += cheby_dist

    sum_distance /= nr_final_states

    return sum_distance



