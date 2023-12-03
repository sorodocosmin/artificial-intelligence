import numpy as np


class QLearning:
    def __init__(self, nr_rows_states, nr_cols_states, nr_actions,
                 start_state, end_state,
                 power_wind_col=False, nr_episodes=200, alpha=0.1, gamma=0.9):
        """
        :param states: will be a matrix, where states[i][j] represents the cell (i, j)
        :param actions: will be a list of possible actions
        """
        if power_wind_col is False:
            self.__power_wind_col = np.zeros(nr_cols_states)
        else:
            self.__power_wind_col = np.array(power_wind_col)

        self.__start_state = start_state
        self.__end_state = end_state

        self.__alpha = alpha
        self.__gamma = gamma
        self.__nr_episodes = nr_episodes
        self.__nr_rows_states = nr_rows_states
        self.__nr_cols_states = nr_cols_states
        self.__nr_actions = nr_actions
        self.__Q = np.zeros((nr_rows_states, nr_cols_states, nr_actions))
        # the Q table will be a 3D matrix,
        # where Q[i][j][k] represents the Q value for the state (i, j) and action k

    def train(self):
        self.__reward_per_episode = []
        for i in range(self.__nr_episodes):
            print(f"episode {i}")
            reward = 0
            current_state = self.__start_state
            while current_state != self.__end_state:
                # choose an action
                action = self.__choose_action_normal(current_state)
                # action = self.__choose_action_eps_greedy(current_state)
                # print(f"action: {action}")
                prev_state = current_state
                current_state = self.__get_next_state(current_state, action)
                # print(f"prev state: {prev_state} ; next state: {current_state}")
                self.__update_Q(prev_state, current_state, action)
                reward += self.__Q[prev_state[0]][prev_state[1]][action]
            self.__reward_per_episode.append(reward)

    def __update_Q(self, prev_state, current_state, action):
        row, col = prev_state
        next_row, next_col = current_state
        q_state = self.__Q[row][col][action]
        self.__Q[row][col][action] = q_state + self.__alpha * (
            self.get_recompense(next_row, next_col) + self.__gamma * (
                self.get_max_value_of_possible_actions((next_row, next_col))[0] - q_state
                )
            )

    def __choose_action_normal(self, state):
        # returns the action for which the Q value is the highest

        maxi_val, imp_actions = self.get_max_value_of_possible_actions(state)
        row, col = state
        possible_actions = [act for act in range(self.__nr_actions)
                            if act not in imp_actions and
                            self.__Q[row][col][act] == maxi_val]

        # print(f"state({state}) -- val pos actions: {possible_actions}")
        return np.random.choice(possible_actions)

    def __get_next_state(self, state, action):
        # we are sure that the action is valid
        row, col = state
        next_row = row
        next_col = col
        pow_wind = self.__power_wind_col[col]

        next_row -= pow_wind

        if action == 0:  # go up
            next_row = next_row - 1
        elif action == 1:  # go right
            next_col += 1
        elif action == 2:  # go down
            next_row = next_row + 1
        elif action == 3:  # go left
            next_col -= 1

        # in case the wind is too strong, we cannot exit the grid
        next_row = max(0, next_row)
        next_row = min(self.__nr_rows_states - 1, next_row)

        return next_row, next_col

    def get_max_value_of_possible_actions(self, state):
        """
        :return: the maximum value of the Q table for the possible actions
        """
        # 0 -> action up;
        # 1 -> action right;
        # 2 -> action down;
        # 3 -> action left;
        row, col = state
        imp_actions = set()
        if row == 0:  # cannot go up
            imp_actions.add(0)
        if col == 0:  # cannot go left
            imp_actions.add(3)
        if row == self.__nr_rows_states - 1:  # cannot go down
            imp_actions.add(2)
        if col == self.__nr_cols_states - 1:  # cannot go right
            imp_actions.add(1)

        maxi_val = None
        for action, val in enumerate(self.__Q[row][col]):
            if action not in imp_actions:
                if maxi_val is None:
                    maxi_val = val
                elif maxi_val < val:
                    maxi_val = val

        return maxi_val, imp_actions

    def get_policy(self):
        current_state = self.__start_state
        list_policy = [current_state]
        while current_state != self.__end_state:
            action = self.__choose_action_normal(current_state)
            print(f"state: {current_state} ; action: {action}")
            current_state = self.__get_next_state(current_state, action)
            list_policy.append(current_state)

        print(f"state: {current_state}")
        return list_policy

    def get_reward_per_episode(self):
        return self.__reward_per_episode

    def get_recompense(self, i, j):
        if (i, j) == self.__end_state:
            return 999_999.999
        return -1



