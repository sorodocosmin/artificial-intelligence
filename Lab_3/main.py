
import time
from table_sudoku import TableSudoku
from matrix_rules import MatrixRules
import copy


def create_sudoku_1():
    #  we will consider that the input of the sudoku will be a valid one
    sdk = TableSudoku()
    # first row
    sdk.set_cell(1, 1, 8)
    sdk.set_cell(1, 2, 4)
    sdk.set_cell(1, 5, 5)
    sdk.set_cell(1, 5, 5)
    sdk.set_gray_cell(1, 7)
    # second row
    sdk.set_cell(2, 1, 3)
    sdk.set_cell(2, 4, 6)
    sdk.set_cell(2, 6, 8)
    sdk.set_cell(2, 8, 4)
    # third row
    sdk.set_gray_cell(3, 3)
    sdk.set_cell(3, 4, 4)
    sdk.set_cell(3, 6, 9)
    sdk.set_gray_cell(3, 9)
    # fourth row
    sdk.set_cell(4, 2, 2)
    sdk.set_cell(4, 3, 3)
    sdk.set_gray_cell(4, 5)
    sdk.set_cell(4, 7, 9)
    sdk.set_cell(4, 8, 8)
    # fifth row
    sdk.set_cell(5, 1, 1)
    sdk.set_gray_cell(5, 4)
    sdk.set_gray_cell(5, 6)
    sdk.set_cell(5, 9, 4)
    # sixth row
    sdk.set_cell(6, 2, 9)
    sdk.set_cell(6, 3, 8)
    sdk.set_gray_cell(6, 5)
    sdk.set_cell(6, 7, 1)
    sdk.set_cell(6, 8, 6)
    # seventh row
    sdk.set_gray_cell(7, 1)
    sdk.set_cell(7, 4, 5)
    sdk.set_cell(7, 6, 3)
    sdk.set_gray_cell(7, 7)
    # eighth row
    sdk.set_cell(8, 2, 3)
    sdk.set_cell(8, 4, 1)
    sdk.set_cell(8, 6, 6)
    sdk.set_cell(8, 9, 7)
    # ninth row
    sdk.set_gray_cell(9, 3)
    sdk.set_cell(9, 5, 2)
    sdk.set_cell(9, 8, 1)
    sdk.set_cell(9, 9, 3)

    return sdk


def create_sudoku_2():
    # populate only the first line
    sdk = TableSudoku()
    sdk.set_cell(1, 1, 1)
    sdk.set_cell(1, 2, 2)
    sdk.set_cell(1, 3, 3)
    sdk.set_cell(1, 4, 4)
    sdk.set_cell(1, 5, 5)
    sdk.set_cell(1, 6, 6)
    sdk.set_cell(1, 7, 7)
    sdk.set_cell(1, 8, 8)
    sdk.set_cell(1, 9, 9)

    return sdk


def BKT_with_FC_and_MRV(rules):
    if rules.is_complete():
        return rules

    pos_i_var, pos_j_var, var = rules.get_next_unassigned_variable_MRV()

    for value in var.domain:

        if rules.are_consistent_with(pos_i_var, pos_j_var, value):
            old_rules = copy.deepcopy(rules)

            var.set_domain([value])
            rules.update_domains_FC(pos_i_var, pos_j_var)

            if not rules.domain_unassigned_variable_is_empty():
                result = BKT_with_FC_and_MRV(rules)
                if result is not None:
                    return result
                else:
                    rules = old_rules
                    var = rules.matrix_variables[pos_i_var][pos_j_var]

            else:
                rules = old_rules
                var = rules.matrix_variables[pos_i_var][pos_j_var]

    return None


def arc_consistency(rules):
    q = set()  # q will be a set as we don't want to have duplicates
    size = len(rules.matrix_variables)
    for i1 in range(size):
        for j1, var1 in enumerate(rules.matrix_variables[i1]):
            # for every variable in the matrix, we add the arcs to the queue
            # on line
            for j2, var2 in enumerate(rules.matrix_variables[i1]):
                if j1 != j2:
                    q.add(((i1, j1), (i1, j2)))
            # on column
            for i2 in range(size):
                if i1 != i2:
                    q.add(((i1, j1), (i2, j1)))
            # on square
            square_i = i1 // 3
            square_j = j1 // 3
            for i3 in range(square_i * 3, square_i * 3 + 3):
                for j3 in range(square_j * 3, square_j * 3 + 3):
                    if not(i1 == i3 and j1 == j3):
                        q.add(((i1, j1), (i3, j3)))

    while len(q) != 0:
        X, Y = q.pop()
        if remove_inconsistent_values(X, Y, rules):
            for j, var in enumerate(rules.matrix_variables[X[0]]):
                if j != X[1] and var.assigned == False:
                    q.add(((X[0], j), X))
            for i in range(size):
                if i != X[0] and rules.matrix_variables[i][X[1]].assigned == False:
                    q.add(((i, X[1]), X))
            square_i = X[0] // 3
            square_j = X[1] // 3
            for i in range(square_i * 3, square_i * 3 + 3):
                for j in range(square_j * 3, square_j * 3 + 3):
                    if not (X[0] == i and X[1] == j) and rules.matrix_variables[i][j].assigned == False:
                        q.add(((i, j), X))


def remove_inconsistent_values(X, Y, rules):
    removed = False
    for value in rules.matrix_variables[X[0]][X[1]].domain:
        value_in_y_allows = False
        for value_y in rules.matrix_variables[Y[0]][Y[1]].domain:
            if value != value_y:
                value_in_y_allows = True

        if not value_in_y_allows:
            rules.matrix_variables[X[0]][X[1]].domain.remove(value)
            removed = True

    return removed


print("\n-----------------SOLUTION SUDOKU 1-----------------\n")
sudoku_1 = create_sudoku_1()
rules_sdk = MatrixRules(sudoku_1)
# arc_consistency(rules_sdk)
res = BKT_with_FC_and_MRV(rules_sdk)  # result is a MatrixRules object, with rules completed or None if no solution
res.print_domains()

print("\n-----------------SOLUTION SUDOKU 2-----------------\n")
sudoku_2 = create_sudoku_2()
rules_sdk = MatrixRules(sudoku_2)
res = BKT_with_FC_and_MRV(rules_sdk)
res.print_domains()


