
class TableSudoku:
    def __init__(self, size=9):
        self.size = size
        self.table = [[(0, False) for _ in range(size)] for _ in range(size)]

    def set_cell(self, row, col, value):
        if value <= 0 or value > self.size:
            print(f'Error: Value needs to be >= 1 and <= {self.size}')
            return

        if 1 <= row <= self.size and 1 <= col <= self.size:
            self.table[row-1][col-1] = (value, False)
        else:
            print(f'Error: Column and row needs to be >= 1 and <= {self.size}')

    def set_gray_cell(self, row, col):
        if 1 <= row <= self.size and 1 <= col <= self.size:
            self.table[row-1][col-1] = (0, True)
        else:
            print(f'Error: Column and row needs to be >= 1 and <= {self.size}')

    def print_table(self):
        for row in self.table:
            for cell in row:
                print(cell[0], end=' ')
            print()