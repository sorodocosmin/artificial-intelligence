from variable import Variable


class MatrixRules:
    def __init__(self, sudoku_table):
        self.matrix_variables = []

        for row in sudoku_table.table:
            list_var = []
            for cell in row:
                if cell[0] != 0:  # already has a value
                    var = Variable([cell[0]], True)
                    list_var += [var]
                else:
                    if cell[1] == True:  # the cell is gray
                        var = Variable([i for i in range(1, sudoku_table.size + 1) if i % 2 == 0])
                        list_var += [var]
                    else:
                        var = Variable([i for i in range(1, sudoku_table.size + 1)])
                        list_var += [var]

            self.matrix_variables += [list_var]

    def get_next_unassigned_variable_MRV(self):
        min_domain = len(self.matrix_variables) + 1
        min_var = None
        pos_i = None
        pos_j = None

        for i, row in enumerate(self.matrix_variables):
            for j, var in enumerate(row):
                if var.assigned == False and len(var.domain) < min_domain:
                    min_domain = len(var.domain)
                    min_var = var
                    pos_i = i
                    pos_j = j

        return pos_i, pos_j, min_var

    def domain_unassigned_variable_is_empty(self):
        for row in self.matrix_variables:
            for var in row:
                if var.assigned == False and len(var.domain) == 0:
                    return True
        return False

    def are_consistent_with(self, pos_i_var, pos_j_var, value) -> bool:
        # check if variables are diff on the line
        for var in self.matrix_variables[pos_i_var]:
            if var.assigned == True and var.domain[0] == value:
                return False

        # check if variables are diff on the column
        for row in self.matrix_variables:
            if row[pos_j_var].assigned == True and row[pos_j_var].domain[0] == value:
                return False

        # check if variables are diff on the square
        square_i = pos_i_var // 3
        square_j = pos_j_var // 3
        for i in range(square_i * 3, square_i * 3 + 3):
            for j in range(square_j * 3, square_j * 3 + 3):
                if self.matrix_variables[i][j].assigned == True and self.matrix_variables[i][j].domain[0] == value:
                    return False

        return True

    def update_domains_FC(self, pos_i_var, pos_j_var):

        value = self.matrix_variables[pos_i_var][pos_j_var].domain[0]

        # elim value from vars on the line
        for var in self.matrix_variables[pos_i_var]:
            if var.assigned == False and value in var.domain:
                var.domain.remove(value)

        # elim value from vars on the column
        for var in self.matrix_variables:
            if var[pos_j_var].assigned == False and value in var[pos_j_var].domain:
                var[pos_j_var].domain.remove(value)

        # elim value from vars on the square
        square_i = pos_i_var // 3
        square_j = pos_j_var // 3
        for i in range(square_i * 3, square_i * 3 + 3):
            for j in range(square_j * 3, square_j * 3 + 3):
                if self.matrix_variables[i][j].assigned == False and value in self.matrix_variables[i][j].domain:
                    self.matrix_variables[i][j].domain.remove(value)

    def is_complete(self) -> bool:
        for row in self.matrix_variables:
            for var in row:
                if var.assigned == False:
                    return False
        return True

    def print_domains(self):
        for row in self.matrix_variables:
            for var in row:
                print(var.domain, end=' ')
            print()
