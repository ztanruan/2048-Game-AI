# Import game state, action and player class, random module
Game2048State = __import__('2048_game').Game2048State
Game2048Action = __import__('2048_game').Game2048Action
Game2048Player = __import__('2048_game').Game2048Player
import random
import math
import numpy as np
import torch as tr
import pickle as pk
import matplotlib.pyplot as pt
from torch.nn import Sequential, Linear, Flatten

# Max searching depth
search_max_depth = 0

# Processed tree nodes
processed_nodes = 0

# #4
# Generate NN module
# return type: torch.nn.Module
# Tiancheng Dai NN
def getNet(board_size):
    return Sequential(
        Flatten(),
        Linear(in_features=board_size*board_size,out_features=board_size),
        Linear(in_features=board_size,out_features=1)
    )

## ZHEN XIN TAN RUAN NEURAL NETWORK
# def getNet(board_size):
#     return Sequential(
#         Flatten(),
#         Linear(in_features=board_size*board_size,out_features=board_size),
#         Linear(in_features=board_size,out_features=64),
#         Linear(in_features=64,out_features=128),
#         Linear(in_features=128,out_features=64),
#         Linear(in_features=64,out_features=board_size),
#         ReLU()
#     )

## DIANA ZHENG NEURAL NETWORK
# def getNet(board_size):
#     return Sequential(
#         Flatten(),
#         Linear(in_features=board_size*board_size,out_features=board_size),
#         Linear(in_features=board_size,out_features=int(board_size/2)),
#         Linear(in_features=int(board_size/2),out_features=1)
#     )

## KEVIN KHA NEURAL NETWORK
# def getNet(board_size):
#     return Sequential(
#         Flatten(),
#         Linear(in_features=board_size*board_size,out_features=10),
#         Linear(10,8),
#         Linear(8,4),
#         Linear(4,2),
#         Linear(2,1)
#     )

# #5
# Estimates utility of node
# Takes a instance of Node class as input, estimate its utility using NN module generate by function getNet
# return: estimated utility, type int
def nn_utility(node):
    # NN instance
    net = getNet(node.state.size)
    net.load_state_dict(tr.load("model%d.pth" % node.state.size))

    # Predicted NN factor
    return net(tr.tensor([node.state.board]).float()).flatten()[0]

# Tree search node class
class Node(object):
    def __init__(self, state, player):
        self.state = state
        self.player = player

    # #6
    # Calculate utility of state
    # Modify this function, so it adds the return value of nn_utility to the utility result
    def getUtility(self):
        utility = 0
        empty_count = 0

        # Sum non 0 tile values, times factor
        # factor = log2(tile)
        # Count num of zero tiles
        for i in range(self.state.board.shape[0]):
            for j in range(self.state.board.shape[1]):
                if self.state.board[i][j] != 0:
                    utility += self.state.board[i][j] * math.log(self.state.board[i][j], 2)
                else:
                    empty_count += 1

        # More zero tiles = higher utility
        utility += empty_count * 5

        # Add NN factor
        utility += nn_utility(self)

        return utility

# Find next state using expectimax search
def getNextState(state):
    # Reset processed nodes counter
    global processed_nodes
    processed_nodes = 0

    # Update search depth
    depth_map = {2: 5, 4: 1, 6: 1, 8: 1, 10: 1}
    global search_max_depth
    search_max_depth = depth_map[state.size]

    # Find next best move    
    next_node = expectimax(Node(state, Game2048Player.USER), 0)

    # Next state result and number of processed tree nodes
    return next_node.state

# Expectimax tree search
def expectimax(node, depth):
    # Increase tree node counter
    global processed_nodes
    processed_nodes += 1

    # Max or Exp the node
    if node.player == Game2048Player.USER: return findMax(node, depth)
    if node.player == Game2048Player.GAME: return findExp(node, depth)

# Find max state
def findMax(node, depth):
    # Best next move
    next_node = None

    # List all possible next nodes
    next_nodes = []
    valid_actions = node.state.validActions()
    for action in valid_actions:
        if (action == Game2048Action.SLIDE_UP):
            next_state = node.state.slideUp()
            next_nodes.append(Node(next_state, Game2048Player.GAME))
        elif (action == Game2048Action.SLIDE_DOWN):
            next_state = node.state.slideDown()
            next_nodes.append(Node(next_state, Game2048Player.GAME))
        elif (action == Game2048Action.SLIDE_LEFT):
            next_state = node.state.slideLeft()
            next_nodes.append(Node(next_state, Game2048Player.GAME))
        elif (action == Game2048Action.SLIDE_RIGHT):
            next_state = node.state.slideRight()
            next_nodes.append(Node(next_state, Game2048Player.GAME))
        elif (action == Game2048Action.ROTATE_CW):
            next_state = node.state.rotateCenterCW()
            next_nodes.append(Node(next_state, Game2048Player.GAME))
        elif (action == Game2048Action.ROTATE_CCW):
            next_state = node.state.rotateCenterCCW()
            next_nodes.append(Node(next_state, Game2048Player.GAME))
    
    # Find optimal board
    max_utility = float('-inf')
    for n in next_nodes:
        expected_utility = expectimax(n, depth + 1)
        if (expected_utility > max_utility): next_node = n; max_utility = expected_utility
    
    # Next move
    if next_node == None: return node
    else: return next_node

# Find expected state
def findExp(node, depth):
    if depth >= search_max_depth: return node.getUtility()

    # Expected utility
    expected_utility = 0.0

    # All possible next nodes
    next_nodes = []

    # Add all possible next nodes with new tile value of 2
    for i in range(node.state.board.shape[0]):
        for j in range(node.state.board.shape[1]):
            if (node.state.board[i][j] == 0):
                next_state = Game2048State(node.state.size)
                next_state.board = np.copy(node.state.board)
                next_state.board[i][j] = 2
                next_nodes.append(Node(next_state, Game2048Player.USER))

    # Add all possible next nodes with new tile value of 4
    for i in range(node.state.board.shape[0]):
        for j in range(node.state.board.shape[1]):
            if (node.state.board[i][j] == 0):
                next_state = Game2048State(node.state.size)
                next_state.board = np.copy(node.state.board)
                next_state.board[i][j] = 4
                next_nodes.append(Node(next_state, Game2048Player.USER))

    # Sum up expected utility
    for n in next_nodes:
        expected_utility += 1/len(next_nodes) * expectimax(n, depth + 1).getUtility()
    
    # Expected utility result
    return expected_utility

if __name__ == "__main__":
    for board_size in [2,4,6,8,10]:
        # NN instance
        net = getNet(board_size)

        # Load training data
        with open("data%d.pkl" % board_size,"rb") as f: (x, y_targ) = pk.load(f)

        # Prepare training data
        train_loss = []
        shuffle = np.random.permutation(range(len(x)))
        train = shuffle[:-10]

        # Gradient descent
        optimizer = tr.optim.Adam(net.parameters())

        ## DIANA ZHENG OPTIMIZER
        # optimizer = tr.optim.AdamW(net.parameters())

        ## KEVIN KHA OPTIMIZER
        # optimizer = tr.optim.Adamax(net.parameters())
        for epoch in range(1000):
            optimizer.zero_grad()
            y_train = net(x[train])
            e_train = tr.sum((y_train - y_targ[train])**2)
            e_train.backward()
            optimizer.step()
            train_loss.append(e_train.item() / (len(shuffle)-10))

        # Save trained data
        tr.save(net.state_dict(), "model%d.pth" % board_size)
        
        # Plot iteration vs. average loss
        pt.plot(train_loss,'b-')
        pt.legend(["Train"])
        pt.xlabel("Iteration" )
        pt.ylabel("Average Loss")
        pt.title("Iteration vs. Average Loss - %dx%d game size" % (board_size, board_size))
        pt.show()
        
        # Plot actual output vs. target loss
        pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(),'bo')
        pt.legend(["Train"])
        pt.xlabel("Actual output")
        pt.ylabel("Target output")
        pt.title("Actual output vs. Target output - %dx%d game size" % (board_size, board_size))
        pt.show()