# Interactive 2048 game played by AI
# Each move played by AI should be presented and confirmed by user
Game2048State = __import__('2048_game').Game2048State
Game2048Action = __import__('2048_game').Game2048Action
Game2048Player = __import__('2048_game').Game2048Player
import baseline_ai as base_ai
import expectimax_ai as expect_ai


if __name__ == "__main__":
	while True:
		#Ask user for game board size
		size = int(input("Enter game board size (2, 4, 6, 8 or 10): "))

		if (size not in [2, 4, 6, 8, 10]):
			print("Board size invalid")
			continue
		state = Game2048State(size)
		state = state.initialState()

		ai_type = int(input("Which AI should be used? 1: Baseline, 2: Tree Search (Expectimax) :"))

		if (ai_type not in [1,2]):
			print("Please choose 1 for Baseline AI or 2 for Tree Search AI")
			continue
		break

	while True:
		game_ending_state = state.isGameEnded()
		if (game_ending_state[0]):
			if (game_ending_state[1] == Game2048Player.GAME): print("Game Over, lost"); break
			else: print("Game Over, won"); break

		print("Next State: ")
		print(state) #Not printing? Weird

		if (ai_type == 1):
			state = base_ai.getNextState(state)
		elif (ai_type == 2):
			state = expect_ai.getNextState(state)

		cont = input('------'*size + "Confirm? (Enter)")
		state = state.addNewTile()