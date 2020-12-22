Game2048State = __import__('2048_game').Game2048State
Game2048Action = __import__('2048_game').Game2048Action
Game2048Player = __import__('2048_game').Game2048Player
BaselineAI = __import__('baseline_ai')
ExpectimaxAI = __import__('expectimax_ai')

import math
import numpy as np

# Calculate utility of state
def getUtility(state):
    utility = 0
    empty_count = 0

    # Sum non 0 tile values, times factor
    # factor = log2(tile)
    # Count num of zero tiles
    for i in range(state.board.shape[0]):
        for j in range(state.board.shape[1]):
            if state.board[i][j] != 0:
                utility += state.board[i][j] * math.log(state.board[i][j], 2)
            else:
                empty_count += 1

    # More zero tiles = higher utility
    utility += empty_count * 5

    return utility

if __name__ == "__main__":
    # Experiment inputs:
    experiment_ai = BaselineAI
    # experiment_ai = ExpectimaxAI
    board_size = 10

    # ==============================DO NOT MODIFY ANYTHING BELOW THIS LINE==============================

    # Outputs
    utilities = []
    processed_nodes = []

    # Play 100 games:
    for i in range(0, 100):
        # Prompt
        print("Running game %d" % (i + 1))

        # Processed nodes in this game
        nodes_tracker = []

        # Initial state
        state = Game2048State(board_size)
        state = state.initialState()

        # Play game
        while True:
            # AI plays
            state = experiment_ai.getNextState(state)
            if experiment_ai == ExpectimaxAI: nodes_tracker.append(int(ExpectimaxAI.processed_nodes))
            if (state.isGameEnded()[0] == True): utilities.append(int(getUtility(state))); processed_nodes.append(nodes_tracker); break

            # Generate new tiles
            state = state.addNewTile()
            if (state.isGameEnded()[0] == True): utilities.append(int(getUtility(state))); processed_nodes.append(nodes_tracker); break

    # Print results
    print(utilities)
    print(sum(utilities) / len(utilities))
    
    # Fill gap in processed_nodes
    max_length = 0
    for nodes in processed_nodes:
        if len(nodes) > max_length: max_length = len(nodes)
    for nodes in processed_nodes:
        nodes += [0] * (max_length - len(nodes))

    # Output results to CSV
    utilities_np = np.asarray(utilities)
    utility_file_name = "utilities_" + str(board_size) + "_"
    if (experiment_ai) == BaselineAI: utility_file_name += "baseline.csv"
    if (experiment_ai) == ExpectimaxAI: utility_file_name += "expectimax.csv"
    np.savetxt(utility_file_name, utilities_np, delimiter=",")

    if experiment_ai == ExpectimaxAI:
        nodes_np = np.asarray(processed_nodes)
        nodes_file_name = "nodes_" + str(board_size) + "_expectimax.csv"
        np.savetxt(nodes_file_name, nodes_np, delimiter=",")