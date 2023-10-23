import heuristics
from state import State
import queue


def IDDFS(init_state, max_depth):
    for depth in range(1, max_depth + 1):
        # in dictionary, we'll memorise the matrix and at what depth was visited
        # (if we reach the same matrix, but with a bigger depth, we will continue to explore that matrix_
        visited = {}
        moves = []
        solution = depth_limited_DFS(init_state, depth, visited, moves)
        if solution is not None:
            return moves


def depth_limited_DFS(s, depth, visited, moves):
    if s.is_final():
        return s
    if depth == 0:
        return None

    visited[s] = depth

    possible_states = [s.transition_1(),
                       s.transition_2(),
                       s.transition_3(),
                       s.transition_4()]

    for next_state in possible_states:
        if next_state is not None and (next_state not in visited or visited[next_state] < depth):
            moves.append(next_state)
            res = depth_limited_DFS(next_state, depth - 1, visited, moves)
            if res is not None:
                return res
            moves.pop()

    return None


def greedy(init_state: State, heuristic_function):
    pq = queue.PriorityQueue()
    pq.put((heuristic_function(init_state.matrix), init_state))
    visited = {init_state}  # set
    parent_dictionary = {init_state: False}

    while not pq.empty():
        priority, state = pq.get()

        if state.is_final():
            list_states = [state]
            parent_state = parent_dictionary[state]
            while parent_state is not False:
                list_states += [parent_state]
                parent_state = parent_dictionary[parent_state]

            return list_states  # returns the list of getting to a final state in reverse order

        list_possible_states = [state.transition_1(),
                                state.transition_2(),
                                state.transition_3(),
                                state.transition_4()
                                ]

        for next_state in list_possible_states:
            if next_state is not None and next_state not in visited:
                pq.put((heuristic_function(next_state.matrix), next_state))
                visited.add(next_state)
                parent_dictionary[next_state] = state

    return None


def A_star(init_state):
    came_from = {init_state : False}
    d = {init_state: 0}
    f = {init_state: 0}

    pq = queue.PriorityQueue()
    pq.put((f[init_state], init_state))

    while not pq.empty():
        priority, state = pq.get()

        if state.is_final():
            list_states = [state]
            parent_state = came_from[state]

            while parent_state is not False:
                list_states += [parent_state]
                parent_state = came_from[parent_state]

            return list_states

        list_possible_states = [state.transition_1(),
                                state.transition_2(),
                                state.transition_3(),
                                state.transition_4()
                                ]

        for next_state in list_possible_states:
            if (next_state is not None and
                    (next_state not in d or d[next_state] > d[state] +
                     heuristics.hamming_heuristic_m1_to_m2(state.matrix, next_state.matrix))):

                d[next_state] = d[state] + heuristics.hamming_heuristic_m1_to_m2(state.matrix, next_state.matrix)
                f[next_state] = d[next_state] + heuristics.hamming_heuristic(next_state.matrix)
                came_from[next_state] = state
                pq.put((f[next_state], next_state))

    return None
