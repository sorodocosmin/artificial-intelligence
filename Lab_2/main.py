from state import State
import time

def IDDFS(init_state, max_depth):
    for depth in range(1, max_depth+1):
        print(f"depth={depth}")
        visited = set()
        moves = []
        solution = depth_limited_DFS(init_state, depth, visited, moves)
        if solution is not None:
            return solution, moves


def depth_limited_DFS(s, depth, visited, moves):
    if s.is_final():
        return s, moves
    if depth == 0:
        return None

    visited.add(s)

    possible_states = [s.transition_1(),
                       s.transition_2(),
                       s.transition_3(),
                       s.transition_4()]
    # print(f"for state : \n{s}")
    for next_state in possible_states:
        if next_state is not None and (next_state not in visited):
            # print(f"------------\n{next_state}\n--------------")
            moves.append(next_state)
            res = depth_limited_DFS(next_state, depth-1, visited, moves)
            if res is not None:
                return res
            moves.pop()

    return None


state_1 = State((8, 6, 7, 2, 5, 4, 0, 3, 1))
state_2 = State((2, 5, 3, 1, 0, 6, 4, 7, 8))
state_3 = State((2, 7, 5, 0, 8, 4, 3, 1, 6))

start_time = time.time()
for i, st in enumerate(IDDFS(state_1,50)[1]):
    print(f"Step {i} :\n{st}\n")

end_time = time.time()
running_time = end_time - start_time

print(f"Running time : {running_time}")

start_time = time.time()
for i, st in enumerate(IDDFS(state_2,50)[1]):
    print(f"Step {i} :\n{st}\n")

end_time = time.time()
running_time = end_time - start_time

print(f"Running time : {running_time}")

start_time = time.time()
for i, st in enumerate(IDDFS(state_3,50)[1]):
    print(f"Step {i} :\n{st}\n")

end_time = time.time()
running_time = end_time - start_time

print(f"Running time : {running_time}")



