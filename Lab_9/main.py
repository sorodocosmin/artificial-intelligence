from q_learning import QLearning
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch


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


def show_policy(num_rows, num_cols, policy):
    fig, ax = plt.subplots()
    ax.set_xlim(0, num_cols)
    ax.set_ylim(0, num_rows)

    ax.set_aspect('equal')

    for i in range(num_rows):
        for j in range(num_cols):
            rect = patches.Rectangle((j, i), 1, 1, edgecolor='black', facecolor='white')
            ax.add_patch(rect)

            action = policy[i][j]
            if action == 2:  # down
                arrow_patch = FancyArrowPatch((j + 0.5, i + 0.1), (j + 0.5, i + 0.9), color='black', arrowstyle='->', mutation_scale=15)
            elif action == 0:  # up
                arrow_patch = FancyArrowPatch((j + 0.5, i + 0.9), (j + 0.5, i + 0.1), color='black', arrowstyle='->', mutation_scale=15)
            elif action == 3:  # left
                arrow_patch = FancyArrowPatch((j + 0.9, i + 0.5), (j + 0.1, i + 0.5), color='black', arrowstyle='->', mutation_scale=15)
            elif action == 1:  # right
                arrow_patch = FancyArrowPatch((j + 0.1, i + 0.5), (j + 0.9, i + 0.5), color='black', arrowstyle='->', mutation_scale=15)

            ax.add_patch(arrow_patch)

            # Color specific cells
            if (i, j) == (3, 0):
                rect.set_facecolor('gray')
            elif (i, j) == (3, 7):
                rect.set_facecolor('green')

    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.show()


# we need to model a problem which has a grid of 7 rows and 10 columns
power_wind_per_column = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
possible_actions = ['up', 'right', 'down', 'left']

q = QLearning(7, 10, 4,
              (3, 0), (3, 7),
              power_wind_per_column, nr_episodes=300)
q.train()
list_path = q.get_path()
show_path(list_path, 7, 10)

policy = q.get_policy()
print(policy)

show_policy(7, 10, policy)

rewards_per_episode = q.get_reward_per_episode()
show_reward_per_ep(rewards_per_episode)

