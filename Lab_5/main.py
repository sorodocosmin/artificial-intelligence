from state import State

# 2 7 6
# 9 5 1
# 4 3 8


def play_game(state):
    while state.is_final() == 0:
        if state.get_player_turn() == 1:
            # My turn to play
            update_state_from_user(state)
        else:
            print("\nAI's turn to play")
            state = get_state_from_AI(state)

    print(state)
    if state.is_final() == 1:
        print("The winner is Player1")
    elif state.is_final() == 2:
        print("The winner is Player2")
    else:
        print("It's a draw")


def get_state_from_AI(state_AI):
    next_states = state_AI.possible_next_states()

    best_state = None
    best_value = float('-inf')

    for state in next_states:
        value = minimax(state, 5, False)
        if value >= best_value:
            best_value = value
            best_state = state

    return best_state


def minimax(state, depth, maximizing_player):
    if depth == 0 or state.is_final() != 0:
        return heuristic(state, maximizing_player)

    if maximizing_player:
        value = float('-inf')
        for child in state.possible_next_states():
            value = max(value, minimax(child, depth - 1, False))
    else:
        value = float('inf')
        for child in state.possible_next_states():
            value = min(value, minimax(child, depth - 1, True))

    return value


def heuristic(state, maximizing_player):
    """
    #directions open for me - #directions open for the opponent
    at every step, self.__player_turn represents the opponent
    :param state:
    :param maximizing_player:
    :return:
    """
    ck_final_state = state.is_final()

    if ck_final_state == 2 or ck_final_state == 1:
        if maximizing_player:
            return float('-inf')
        else:
            return float('inf')

    elif ck_final_state == 3:  # it's a draw
        return 0

    me_player = state.get_player_turn() % 2 + 1
    opponent_player = state.get_player_turn()

    directions_open_for_me = state.open_directions(me_player)
    directions_open_for_opponent = state.open_directions(opponent_player)

    return directions_open_for_me - directions_open_for_opponent


def update_state_from_user(state_user):
    print(state_user)
    ok = False
    while not ok:
        try:
            nr = int(input(f"You (Player{str(state_user.get_player_turn())}) choose a number(1-9): "))
        # catch exception
        except ValueError:
            print("Please enter an integer")
            continue
        if nr < 1 or nr > 9:
            print("Please enter a number between 1 and 9")
            continue
        # check if the cell is empty
        pos_i, pos_j = State.from_nr_scrabble_in_cell(nr)
        if state_user.set_cell(pos_i, pos_j) is False:
            print("Number already used")
            continue
        ok = True


s1 = State(1)

play_game(s1)
