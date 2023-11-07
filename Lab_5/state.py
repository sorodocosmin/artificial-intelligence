import copy


class State:
    """
    [   [2, 7, 6]
        [9, 5, 1]
        [3, 4, 8]
    ]
    """
    def __init__(self, player_turn: int):
        self.__player_turn = player_turn
        self.__board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 0 represents that the cell is empty
        self.__moved_first = player_turn

    def is_final(self):
        """
        :return: 1 - if the player 1 won; 2 - if the player 2 won;
        3 - if it's a draw; 0 - if the game is not over

        """
        if self.__board_full():
            return 3

        ck_rows = self.__check_rows()
        if ck_rows != 0:
            return ck_rows

        ck_columns = self.__check_columns()
        if ck_columns != 0:
            return ck_columns

        ck_diagonals = self.__check_diagonals()
        if ck_diagonals != 0:
            return ck_diagonals

        return 0

    def possible_next_states(self):
        """
        :return: a list of possible next states
        """
        next_states = []
        for i in range(3):
            for j in range(3):
                if self.__board[i][j] == 0:
                    next_state = State(self.__player_turn % 2 + 1)
                    next_state.__board = copy.deepcopy(self.__board)
                    next_state.__board[i][j] = self.__player_turn
                    next_state.__moved_first = self.__moved_first
                    next_states.append(next_state)
        return next_states

    def open_directions(self, player):
        directions = 0
        # check rows
        for i in range(3):
            if ((self.__board[i][0] == 0 or self.__board[i][0] == player) and
                    (self.__board[i][1] == 0 or self.__board[i][1] == player) and
                    (self.__board[i][2] == 0 or self.__board[i][2] == player)):
                directions += 1

        # check columns
        for i in range(3):
            if ((self.__board[0][i] == 0 or self.__board[0][i] == player) and
                    (self.__board[1][i] == 0 or self.__board[1][i] == player) and
                    (self.__board[2][i] == 0 or self.__board[2][i] == player)):
                directions += 1

        # check diagonals
        if ((self.__board[0][0] == 0 or self.__board[0][0] == player) and
                (self.__board[1][1] == 0 or self.__board[1][1] == player) and
                (self.__board[2][2] == 0 or self.__board[2][2] == player)):
            directions += 1

        if ((self.__board[0][2] == 0 or self.__board[0][2] == player) and
                (self.__board[1][1] == 0 or self.__board[1][1] == player) and
                (self.__board[2][0] == 0 or self.__board[2][0] == player)):
            directions += 1

        return directions

    def set_cell(self, i, j):
        if self.__board[i][j] == 0:
            self.__board[i][j] = self.__player_turn
            self.__player_turn = self.__player_turn % 2 + 1
            return True
        return False

    def get_player_turn(self):
        return self.__player_turn

    def get_moved_first(self):
        return self.__moved_first

    def __board_full(self):
        for i in range(3):
            for j in range(3):
                if self.__board[i][j] == 0:
                    return False
        return True

    def __check_rows(self):
        for i in range(3):
            if self.__board[i][0] == self.__board[i][1] == self.__board[i][2] != 0:
                return self.__board[i][0]

        return 0

    def __check_columns(self):
        for i in range(3):
            if self.__board[0][i] == self.__board[1][i] == self.__board[2][i] != 0:
                return self.__board[0][i]

        return 0

    def __check_diagonals(self):
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] != 0:
            return self.__board[0][0]
        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] != 0:
            return self.__board[0][2]

        return False

    def __str__(self):

        AI_moves = []
        player_moves = []
        available_moves = []
        for i in range(3):
            for j in range(3):
                if self.__board[i][j] == 2:
                    AI_moves.append(self.from_cell_in_nr_scrabble(i, j))
                elif self.__board[i][j] == 1:
                    player_moves.append(self.from_cell_in_nr_scrabble(i, j))
                else:
                    available_moves.append(self.from_cell_in_nr_scrabble(i, j))

        return f"AI moves: {AI_moves}\nPlayer moves: {player_moves}\nAvailable moves: {available_moves}"



    @staticmethod
    def from_cell_in_nr_scrabble(pos_i, pos_j):
        if pos_i == 0 and pos_j == 0:
            return 2
        elif pos_i == 0 and pos_j == 1:
            return 7
        elif pos_i == 0 and pos_j == 2:
            return 6
        elif pos_i == 1 and pos_j == 0:
            return 9
        elif pos_i == 1 and pos_j == 1:
            return 5
        elif pos_i == 1 and pos_j == 2:
            return 1
        elif pos_i == 2 and pos_j == 0:
            return 4
        elif pos_i == 2 and pos_j == 1:
            return 3
        else:
            return 8

    @staticmethod
    def from_nr_scrabble_in_cell(nr_cell):
        if nr_cell == 2:
            return 0, 0
        elif nr_cell == 7:
            return 0, 1
        elif nr_cell == 6:
            return 0, 2
        elif nr_cell == 9:
            return 1, 0
        elif nr_cell == 5:
            return 1, 1
        elif nr_cell == 1:
            return 1, 2
        elif nr_cell == 4:
            return 2, 0
        elif nr_cell == 3:
            return 2, 1
        else:
            return 2, 2

