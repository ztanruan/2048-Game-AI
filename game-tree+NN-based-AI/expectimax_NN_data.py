import torch as tr
import numpy as np
import pickle as pk
Game2048State = __import__('2048_game').Game2048State
import expectimax_ai as expect_ai

# #1
# Encode a 2048_game.Game2048State
# Will be called by get_batch
# return a tensor
def encode(state):
    return tr.from_numpy(state.board).float()
    
# #2
# Generate training data for NN
# Needs to call encode function to encode state
# return: (input, output)
# input: stacked list of encoded states
# output: stacked list of correspond utilities
def get_batch(board_size, num_games):
    inputs = []
    outputs = []

    # Perform 25 games
    for _ in range(0, 25):
        # Start new game
        state = Game2048State(board_size)
        state = state.initialState()

        # Iterate num_games times
        for i in range(0, num_games):
            # Game ended
            if state.isGameEnded()[0]: break

            # Record state
            inputs.append(encode(state))

            # Tree search next state
            state = expect_ai.getNextState(state)

            # Utility of tree searched state
            node = expect_ai.Node(state, None)
            outputs.append(tr.tensor([node.getUtility()]))

            # Add new tile to the game
            state = state.addNewTile()
        
    # Stack tensor
    inputs = tr.stack(inputs)
    outputs = tr.stack(outputs)

    # Result
    return (inputs, outputs)

# #3
# Generate training data file
# Call get_batch function, save training data as a ".pkl" file
if __name__ == "__main__":
    for board_size in [2,4,6,8,10]:
        print("Working on data%d.pkl..." % board_size)
        num_games = 50
        with open("data%d.pkl" % board_size, "wb") as f: pk.dump(get_batch(board_size, num_games), f)
        print("data%d.pkl generated" % board_size)