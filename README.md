# SU CIS667 Semester Project 2048 Game AI
## About
Command line 2048 game, written in Python 3. With slight modification to the original game rule: the agent can also choose to rotate the tiles in the 2x2 square in the middle of the board by +/- 90 degrees. Game can be played manually by user or by AI.

## Dependencies
Python 3.4 or above is required. Make sure following Python dependencies are installed before executing the game:
1. [numpy](https://numpy.org/)

## Execution
1. Clone project to local
```
git clone https://github.com/michaeldai1006/SU-CIS667-semester-project-2048.git
```
2. Change directory to project home directory
```
cd ./SU-CIS667-semester-project-2048
```
3. Run standard game file
```
python3 ./game/2048_game.py
```

3. Run AI game file
```
python3 ./game-tree-based-AI/ai_game.py
```

4. Run NN enhanced tree search AI game file
```
python3 ./game-tree+NN-based-AI/ai_game.py
```

## Standard Game Play
Provide game board size when seeing following command line prompt:
```
Enter game board size (4, 6 or 8): 
```
At the beginning of each turn the current game state will be printed. You will also be provided a list of valid actions in [], type in your next move accordingly.
```
Current state:
   16    2    0    4

    8    0    0    0

    0    4    0    0

    0    0    0    0
['q = Quit', ''u = Slide Up', 'd = Slide Down', 'l = Slide Left', 'r = Slide Right', 'rc = Rotate Center Clockwise', 'rcc = Rotate Center Counterclockwise']
Enter an action: 
```

## AI Game Play
Provide game board size when seeing following command line prompt, 5 game board sizes supported:
```
Enter game board size (2, 4, 6, 8 or 10): 
```
Choose which AI algorithm to use by typing 1 or 2:
```
Which AI should be used? 1: Baseline, 2: Tree Search (Expectimax) :
```
When AI has made their move, the game will print out the next game board state to let you confirm:
```
Next State: 
    2    0    0    0

    0    0    0    0

    4    0    0    0

    0    0    0    0
------------------------Confirm? (Enter)
```
Hold down the enter key to fast forward

## NN enhanced AI Game Play
Provide game board size when seeing following command line prompt, 5 game board sizes supported:
```
Enter game board size (2, 4, 6, 8 or 10): 
```
Choose which AI algorithm to use by typing 1, 2 or 3:
```
Which AI should be used? 1: Baseline, 2: Tree Search (Expectimax), 3: Tree Search (Expectimax) + NN:
```
When AI has made their move, the game will print out the next game board state to let you confirm:
```
Next State: 
    2    0    0    0

    0    0    0    0

    4    0    0    0

    0    0    0    0
------------------------Confirm? (Enter)
```
Hold down the enter key to fast forward

## Credits
tdai06, kkha, dyzheng, ztanruan all rights reserved.