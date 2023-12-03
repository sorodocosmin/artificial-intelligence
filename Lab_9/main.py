import numpy as np

from q_learning import QLearning
import matplotlib.pyplot as plt


def show_path(list_points, rows, cols):
    # Extract x and y coordinates from the points
    rows_points, cols_points = zip(*list_points)

    # Plot the points
    plt.scatter(cols_points, rows_points, color='red', marker='o')

    # Plot lines connecting adjacent points
    for i in range(len(list_points) - 1):
        plt.plot([list_points[i][1], list_points[i + 1][1]], [list_points[i][0], list_points[i + 1][0]], color='blue')

    # Set axis labels
    plt.xlabel('Columns')
    plt.ylabel('Rows')

    # Set grid dimensions
    plt.xticks(range(0, cols+1))
    plt.yticks(range(0, rows+1))

    # Display the graph
    plt.grid(True)
    plt.gca().invert_yaxis()

    plt.show()


def show_reward_per_ep(list_rew):
    plt.plot(range(len(list_rew)), list_rew)
    plt.xlabel('Episodes')
    plt.ylabel('Reward')
    plt.show()


# we need to model a problem which has a grid of 7 rows and 10 columns
power_wind_per_column = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
possible_actions = ['up', 'right', 'down', 'left']

q = QLearning(7, 10, 4,
              (3, 0), (3, 7),
              power_wind_per_column)
q.train()
list_policy = q.get_policy()
show_path(list_policy, 7, 10)

rewards_per_episode = q.get_reward_per_episode()
show_reward_per_ep(rewards_per_episode)

