"""
2048 game file
2048 game state, game operations and interactive game entry point
Students: tdai06, kkha, dyzheng, ztanruan
"""

"""
Packages
"""
import numpy as np
from enum import Enum
import random

"""
Enum that indicates different players of the game
GAME - player game
USER - player user
"""
class Game2048Player(Enum):
    GAME = 'game'
    USER = 'user'

"""
Enum that indicates different actions available to player
"""
class Game2048Action(Enum):
    SLIDE_UP = 1
    SLIDE_DOWN = 2
    SLIDE_LEFT = 3
    SLIDE_RIGHT = 4
    ROTATE_CW = 5
    ROTATE_CCW = 6

"""
Represents current game state and available game operations
"""
class Game2048State(object):
    """
    Init game board with size
    """
    def __init__(self, size):
        # Game board size
        self.size = size

        # Empty game board, 0 indicates a empty tile
        self.board = np.empty((size, size),dtype=np.int)
        self.board[:] = 0

    """
    Return a string representation of the current game board
    """
    def __str__(self):
        string_rep = ""
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                string_rep = string_rep + '{:5}'.format(self.board[i][j])
            if(i != self.board.shape[0]-1):
                string_rep = string_rep +'\n\n'
        return string_rep

    """
    Initialize game, generate 2 new tiles with value of either 2 or 4 at random locations
    Return a new game state instance instead of modify the current game state
    """
    def initialState(self):    
        # Add two new tiles    
        new_state = self.addNewTile()
        new_state = new_state.addNewTile()

        return new_state

    """
    Add a new tile at a random empty spot with value of either 2 or 4
    Return a new game state instance instead of modify the current game state
    """
    def addNewTile(self):
        # New game state, copy game board
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)

        # Count empty tiles
        num_empty = np.count_nonzero(new_state.board==0)

        # If no empty spot left, return unmodified state
        if num_empty == 0: return new_state
        
        # New tile index
        index = np.random.randint(0, num_empty)

        # Add tile
        counter = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if new_state.board[i][j] == 0:
                    if counter == index:
                        new_state.board[i][j] = np.random.choice([2,4])
                        return new_state
                    else:
                        counter += 1
    
        return new_state

    """
    Slide the tiles up, merge tiles if needed
    Return a new game state instance instead of modify the current game state
    """
    def slideUp(self):
        # New game state, copy game board
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)

        b = new_state.board
        #This sums everything as long as there are only 0's (or nothing) between them
        for c in range(0, self.size):
            r = 0
            while r < self.size:
                for temp_r in range(r+1, self.size):
                    if b[temp_r][c] != 0 and b[r][c] != b[temp_r][c]:
                        #If we find a num not 0, we change r to that number
                        r = temp_r
                    elif b[r][c] != 0 and b[r][c] == b[temp_r][c]:
                        #If we find two numbers that are the same, sum them
                        #and zero out the 2nd location
                        b[r][c] = b[r][c] * 2
                        b[temp_r][c] = 0
                        r = temp_r
                        temp_r +=1
                r +=1

        #to slide everything up now, already summed.
        for r in range(0, self.size):
            for c in range(0, self.size):
                for temp_r in range(r, self.size):
                    if b[temp_r][c] == 0:
                        #If it's 0, we don't care.
                        temp_r +1
                    elif temp_r != r and b[r][c] == 0:
                        #If it's not 0, we bring it to the most up 0.
                        b[r][c] = b[temp_r][c]
                        b[temp_r][c] = 0

        return new_state

    """
    Slide the tiles down, merge tiles if needed
    Return a new game state instance instead of modify the current game state
    """
    def slideDown(self):
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)

        #Simply rotating the board to use SlideUp, then rotating it back
        new_state.board = np.rot90(new_state.board, 2)
        new_state = new_state.slideUp()
        new_state.board = np.rot90(new_state.board, 2)

        return new_state

    """
    Slide the tiles toward left, merge tiles if needed
    Return a new game state instance instead of modify the current game state
    """
    def slideLeft(self):
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)

        #Simply rotating the board to use SlideUp, then rotating it back
        new_state.board = np.rot90(new_state.board, 3)
        new_state = new_state.slideUp()
        new_state.board = np.rot90(new_state.board, 1)
        return new_state

    """
    Slide the tiles toward right, merge tiles if needed
    Return a new game state instance instead of modify the current game state
    """
    def slideRight(self):
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)

        #Simply rotating the board to use SlideUp, then rotating it back
        new_state.board = np.rot90(new_state.board, 1)
        new_state = new_state.slideUp()
        new_state.board = np.rot90(new_state.board, 3)

        return new_state
    
    """
    Rotate the center 2x2 square clockwise for 90 degrees
    Return a new game state instance instead of modify the current game state
    """
    def rotateCenterCW(self):
        # New game state, copy game board
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)

        # Rotate center
        rot_bd = int(self.size / 2 - 1)
        new_state.board[rot_bd:rot_bd + 2, rot_bd:rot_bd + 2] = np.rot90(self.board[rot_bd:rot_bd + 2, rot_bd:rot_bd + 2], 3)

        # Rotated state
        return new_state

    """
    Rotate the center 2x2 square counterclockwise for 90 degrees
    Return a new game state instance instead of modify the current game state
    """
    def rotateCenterCCW(self):
        # New game state, copy game board
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)
        
        # Rotate center
        rot_bd = int(self.size / 2 - 1)
        new_state.board[rot_bd:rot_bd + 2, rot_bd:rot_bd + 2] = np.rot90(self.board[rot_bd:rot_bd + 2, rot_bd:rot_bd + 2])

        # Rotated state
        return new_state
    
    """
    Return a list of valid actions
    Example: [Game2048Action.SLIDE_UP, Game2048Action.ROTATE_CW, Game2048Action.ROTATE_CCW]
    """
    def validActions(self):       
       new_state = Game2048State(self.size)
       new_state.board = np.copy(self.board)
       b = new_state
       b.board = np.copy(new_state.board)
       
       actions = []
       new_state = new_state.slideUp()
       if str(b.board) != str(new_state.board):

           actions.append(Game2048Action.SLIDE_UP)
       new_state = b

       new_state = new_state.slideDown()
       if str(b.board) != str(new_state.board):
           actions.append(Game2048Action.SLIDE_DOWN)
       new_state = b

       new_state = new_state.slideLeft()
       if str(b.board) != str(new_state.board):
           actions.append(Game2048Action.SLIDE_LEFT)
       new_state = b
       
       new_state = new_state.slideRight()
       if str(b.board) != str(new_state.board):
           actions.append(Game2048Action.SLIDE_RIGHT)
       new_state = b

       mid = int(self.size / 2)
       midNums = []
       for i in range(mid-1,mid+1):
           for j in range(mid-1,mid+1):
               if not b.board[i][j] in midNums:
                   midNums.append(b.board[i][j])
       if len(midNums) != 1:
           actions.append(Game2048Action.ROTATE_CW)
           actions.append(Game2048Action.ROTATE_CCW)

       return actions

    """
    Check whether current game is ended and find the winner
    return (True, Game2048Player.USER) if tile with value 2048 appears
    return (True, Game2048Player.GAME) if no matter how user rotates the center 2x2 square there are no more than 2 valid actions
    return (False,) if game continues
    """
    def isGameEnded(self):
        # New game state, copy game board
        new_state = Game2048State(self.size)
        new_state.board = np.copy(self.board)

        b = new_state.board
        for r in range(0, self.size):
            for c in range(0, self.size):
                if b[r][c] == 2048:
                    return (True, Game2048Player.USER)
                    #exit()
        actions2 = []
        
        myList = []
        myList.append(Game2048Action.ROTATE_CW)
        myList.append(Game2048Action.ROTATE_CCW)
        if ((new_state.validActions()) == myList):
            b = new_state
            b.board = np.copy(new_state.board)
            c = new_state
            b.board = np.copy(new_state.board)
            b = new_state.rotateCenterCW()
        
            if str(b.board) != str(new_state.board):
                c.board = np.copy(new_state.board)
                new_state = new_state.slideUp()
                if str(c.board) != str(new_state.board):
                    actions2.append(Game2048Action.ROTATE_CW)
                new_state = c
                new_state = new_state.slideDown()
                if str(c.board) != str(new_state.board):
                    if not Game2048Action.ROTATE_CW in actions2:
                        actions2.append(Game2048Action.ROTATE_CW)
                new_state = c
                new_state = new_state.slideLeft()
                if str(c.board) != str(new_state.board):
                    if not Game2048Action.ROTATE_CW in actions2:
                        actions2.append(Game2048Action.ROTATE_CW)
                new_state = c
                new_state = new_state.slideRight()
                if str(c.board) != str(new_state.board):
                    if not Game2048Action.ROTATE_CW in actions2:
                        actions2.append(Game2048Action.ROTATE_CW)
            b = new_state
            
            new_state = new_state.rotateCenterCCW()
            #print(actions2)
            if str(b.board) != str(new_state.board):
                c.board = np.copy(new_state.board)
                new_state = new_state.slideUp()
                if str(c.board) != str(new_state.board):
                    actions2.append(Game2048Action.ROTATE_CCW)
                new_state = c
                new_state = new_state.slideDown()
                if str(c.board) != str(new_state.board):
                    if not Game2048Action.ROTATE_CCW in actions2:
                        actions2.append(Game2048Action.ROTATE_CCW)
                new_state = c
                new_state = new_state.slideLeft()
                if str(c.board) != str(new_state.board):
                    if not Game2048Action.ROTATE_CCW in actions2:
                        actions2.append(Game2048Action.ROTATE_CCW)
                new_state = c
                new_state = new_state.slideRight()
                if str(c.board) != str(new_state.board):
                    if not Game2048Action.ROTATE_CCW in actions2:
                        actions2.append(Game2048Action.ROTATE_CCW)
            b = new_state
            #print(actions2)
            if len(actions2) == 0:
                return (True, Game2048Player.GAME)
        return (False,)

"""
Interactive game entry point
Prompt the user to play the game
"""    
if __name__ == "__main__":
    # Main function constants
    action_map = {
        Game2048Action.SLIDE_UP: "u = Slide Up",
        Game2048Action.SLIDE_DOWN: "d = Slide Down",
        Game2048Action.SLIDE_LEFT: "l = Slide Left",
        Game2048Action.SLIDE_RIGHT: "r = Slide Right",
        Game2048Action.ROTATE_CW: "rc = Rotate Center Clockwise",
        Game2048Action.ROTATE_CCW: "rcc = Rotate Center Counterclockwise"
    }
    action_command = {
        Game2048Action.SLIDE_UP: "u",
        Game2048Action.SLIDE_DOWN: "d",
        Game2048Action.SLIDE_LEFT: "l",
        Game2048Action.SLIDE_RIGHT: "r",
        Game2048Action.ROTATE_CW: "rc",
        Game2048Action.ROTATE_CCW: "rcc"
    }

    while True:
        # Ask user for game board size
        size = int(input("Enter game board size (4, 6 or 8): "))
        
        # Input size invalid
        if (size not in [4, 6, 8]): print("Board size invalid"); continue

        # Init game
        state = Game2048State(size)
        state = state.initialState()
        break

    # Prompt user to perform action
    while True:
        # Check game ending state
        game_ending_state = state.isGameEnded()
        if (game_ending_state[0]):
            if (game_ending_state[1] == Game2048Player.GAME): print("Game Over, you lost"); break
            else: print("Game Over, you won"); break

        # Current game state
        print("Current state:")
        print(state)
        
        # Valid actions for current state
        valid_actions = state.validActions()

        # Prompt user to choose action
        action_prompts = ['q = Quit']; valid_commands = ['q']
        for action in valid_actions: action_prompts.append(action_map[action]); valid_commands.append(action_command[action])
        print(action_prompts) 
        action = input("Enter an action: ")

        # Action not valid, choose again
        if action not in valid_commands: print("Invalid action, please choose again"); continue

        # Perform action
        if (action == 'u'): state = state.slideUp()
        elif (action == 'd'): state = state.slideDown()
        elif (action == 'l'): state = state.slideLeft()
        elif (action == 'r'): state = state.slideRight()
        elif (action == 'rc'): state = state.rotateCenterCW()
        elif (action == 'rcc'): state = state.rotateCenterCCW()
        elif (action == 'q'): break

        # Add new tile to board
        state = state.addNewTile()