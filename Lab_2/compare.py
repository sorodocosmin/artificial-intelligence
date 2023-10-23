from state import State
import time
import main
import heuristics

def run_IDDFS(state, max_depth):
    """
    This function returns a tuple as follows:
    (solution_size, time_execution)
    :param state:
    :param max_depth:
    :return:
    """
    start_time = time.time()
    result = main.IDDFS(state, max_depth)  # returns a list of all states, but not the initial one

    end_time = time.time()
    running_time = end_time - start_time

    if result is not None:
        return result[len(result)-1], len(result), running_time
    else:
        return None, running_time


def run_greedy(state, heuristic_function):
    """
    This function returns a tuple as follows:
    (solution, solution_size, time_execution)
    """
    start_time = time.time()
    result = main.greedy(state, heuristic_function)
    #          |-> returns a list of all states, including the first one (in reverse order)

    end_time = time.time()
    running_time = end_time - start_time

    if result is not None:
        return result[0], len(result)-1, running_time
    else:
        return None, running_time


def run_A_star(state):
    start_time = time.time()
    result = main.A_star(state)
    #          |-> returns a list of all states, including the first one (in reverse order)

    end_time = time.time()
    running_time = end_time - start_time

    if result is not None:
        return result[0], len(result) - 1, running_time
    else:
        return None, running_time


state_1 = State((8, 6, 7, 2, 5, 4, 0, 3, 1))
state_2 = State((2, 5, 3, 1, 0, 6, 4, 7, 8))
state_3 = State((2, 7, 5, 0, 8, 4, 3, 1, 6))


def print_info(state):
    print("----------------------------------------------------------------------------------------------------")
    print(f"For the state :\n{state}\nWe got the following results:")
    res_iddfs = run_IDDFS(state, 50)
    res_greedy_manhattan = run_greedy(state, heuristics.manhattan_heuristic)
    res_greedy_hamming = run_greedy(state, heuristics.hamming_heuristic)
    res_greedy_cheby = run_greedy(state, heuristics.chebyshev_heuristic)
    res_A_star = run_A_star(state)
    print(f"IDDFS (max depth = 50) : solution = \n{res_iddfs[0]}\nsolution size = {res_iddfs[1]}; time = {res_iddfs[2]} s\n")
    print(f"Greedy (manhattan) : solution = \n{res_greedy_manhattan[0]}\nsolution size = {res_greedy_manhattan[1]}; time = {res_greedy_manhattan[2]} s\n")
    print(f"Greedy (hamming) : solution = \n{res_greedy_hamming[0]}\nsolution size = {res_greedy_hamming[1]}; time = {res_greedy_hamming[2]} s\n")
    print(f"Greedy (chebyshev) : solution = \n{res_greedy_cheby[0]}\nsolution size = {res_greedy_cheby[1]}; time = {res_greedy_cheby[2]} s\n")
    print(f"A* : solution = \n{res_A_star[0]}\nsolution size = {res_A_star[1]}; time = {res_A_star[2]} s")
    print("----------------------------------------------------------------------------------------------------")


print_info(state_1)
print_info(state_2)
print_info(state_3)
