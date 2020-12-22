# Import game state and action class, random module
Game2048State = __import__('2048_game').Game2048State
Game2048Action = __import__('2048_game').Game2048Action
import random

# Find next state using baseline AI
def getNextState(state):
    # Random next action
    action = random.choice(state.validActions())

    # Perform action
    result_state = None
    if (action == Game2048Action.SLIDE_UP):
        result_state = state.slideUp()
    elif (action == Game2048Action.SLIDE_DOWN):
        result_state = state.slideDown()
    elif (action == Game2048Action.SLIDE_LEFT):
        result_state = state.slideLeft()
    elif (action == Game2048Action.SLIDE_RIGHT):
        result_state = state.slideRight()
    elif (action == Game2048Action.ROTATE_CW):
        result_state = state.rotateCenterCW()
    elif (action == Game2048Action.ROTATE_CCW):
        result_state = state.rotateCenterCCW()
    
    # Next state
    return result_state

if __name__ == "__main__":
    # AI demo
    state = Game2048State(6)
    state = state.initialState()
    print(state)

    for _ in range(0, 50000):
        state = getNextState(state)
        print(state)
        state = state.addNewTile()
        print(state)