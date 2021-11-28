import math
import random


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ') 
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves()) 
        return square


class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # randomly choose one
            square = random.choice(game.available_moves())
        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            # each score should maximize
            best = {'position': None, 'score': -math.inf}
        else:
            # each score should minimize
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # Step 1: make a random move, try a random position
            state.make_move(possible_move, player)

            # Step 2: simulate a game after making that move
            sim_score = self.minimax(state, other_player)

            # Step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            # this represents the move optimal next move
            sim_score['position'] = possible_move

            # Step 4: update the dictionaries if necessary
            if player == max_player:    # maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score    # replace best
            else:   # minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score    # replace best
        return best
