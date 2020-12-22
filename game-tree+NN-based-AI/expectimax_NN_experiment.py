Game2048State = __import__('2048_game').Game2048State
Game2048Action = __import__('2048_game').Game2048Action
Game2048Player = __import__('2048_game').Game2048Player
BaselineAI = __import__('baseline_ai')
ExpectimaxAI = __import__('expectimax_ai')
Expectimax_NN_ai = __import__('expectimax_NN_ai')

import math
import numpy as np
import matplotlib.pyplot as pt

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
    inputs = [
        [BaselineAI,2,"Baseline AI"],
        [BaselineAI,4,"Baseline AI"],
        [BaselineAI,6,"Baseline AI"],
        [BaselineAI,8,"Baseline AI"],
        [BaselineAI,10,"Baseline AI"],
        [ExpectimaxAI,2,"Expectimax AI"],
        [ExpectimaxAI,4,"Expectimax AI"],
        [ExpectimaxAI,6,"Expectimax AI"],
        [ExpectimaxAI,8,"Expectimax AI"],
        [ExpectimaxAI,10,"Expectimax AI"],
        [Expectimax_NN_ai,2,"Expectimax+NN AI"],
        [Expectimax_NN_ai,4,"Expectimax+NN AI"],
        [Expectimax_NN_ai,6,"Expectimax+NN AI"],
        [Expectimax_NN_ai,8,"Expectimax+NN AI"],
        [Expectimax_NN_ai,10,"Expectimax+NN AI"]        
    ]

    for input in inputs:
        experiment_ai = input[0]
        board_size = input[1]
        ai_name = input[2]

        # Outputs
        utilities = []

        # Play 100 games:
        for i in range(0, 100):
            # Prompt
            print("%s, game size %d, Running game %d/100" % (ai_name, board_size, i + 1))

            # Initial state
            state = Game2048State(board_size)
            state = state.initialState()

            # Play game
            counter = 0
            while True:
                counter += 1
                if counter >= 5000: utilities.append(int(getUtility(state))); break
                # AI plays
                state = experiment_ai.getNextState(state)
                if (state.isGameEnded()[0] == True): utilities.append(int(getUtility(state))); break

                # Generate new tiles
                state = state.addNewTile()
                if (state.isGameEnded()[0] == True): utilities.append(int(getUtility(state))); break
        
        # Plot
        pt.hist(utilities, density=False)
        pt.xlabel("Final Game Score" )
        pt.ylabel("Count")
        pt.title("100 Games Final Score - %dx%d game size, %s" % (board_size, board_size, ai_name))
        pt.savefig("%dx%d-%s" % (board_size, board_size, ai_name))
        pt.clf()
        print("Fig saved")