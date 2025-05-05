"""
Tic Tac Toe class + game play implementation by Kylie Ying
YouTube Kylie Ying: https://www.youtube.com/ycubed 
Twitch KylieYing: https://www.twitch.tv/kylieying 
Twitter @kylieyying: https://twitter.com/kylieyying 
Instagram @kylieyying: https://www.instagram.com/kylieyying/ 
Website: https://www.kylieying.com
Github: https://www.github.com/kying18 
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ 
"""

# Developed by phoenix marie.
import math
import time
from random import randint
import json  # For saving and loading game history


class Player():
    def __init__(self, letter):
        # letter is x or o
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
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Please try again.')
        return val


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = randint(0, 8)
        while square not in game.available_moves():
            square = randint(0, 8)
        return square


class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = randint(0, 8)  # choose one at random
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # base case: if the previous move made someone win
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # simulate a game after making that move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move consistent with the score

            if player == max_player:  # maximize over the max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:  # minimize over the other player
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None
        self.move_history = []  # To store the moves made in the current game

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            self.move_history.append((square, letter))  # Record the move
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        # print('row', row)
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        # print('col', column)
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            # print('diag1', diagonal1)
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            # print('diag2', diagonal2)
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

    def is_tie(self):
        return not self.empty_squares() and self.current_winner is None

    def reset_board(self):
        self.board = self.make_board()
        self.current_winner = None
        self.move_history = []

    def get_game_state(self):
        """Returns the current state of the game as a dictionary."""
        return {
            'board': list(self.board),
            'current_winner': self.current_winner,
            'move_history': list(self.move_history)
        }

    def load_game_state(self, game_state):
        """Loads a game state from a dictionary."""
        if 'board' in game_state and len(game_state['board']) == 9:
            self.board = list(game_state['board'])
        if 'current_winner' in game_state:
            self.current_winner = game_state['current_winner']
        if 'move_history' in game_state:
            self.move_history = list(game_state['move_history'])

    def display_move_history(self):
        """Prints the history of moves made in the current game."""
        if self.move_history:
            print("\n--- Move History ---")
            for move, player in self.move_history:
                print(f"Player {player} moved to square {move}")
        else:
            print("No moves have been made yet.")


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):

            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!")
                return letter  # ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # switches player

        time.sleep(.8)

    if print_game:
        if game.is_tie():
            print('It\'s a tie!')
        elif game.current_winner:
            print(game.current_winner + ' wins!')
    return game.current_winner  # Return the winner or None for a tie


def play_again():
    while True:
        response = input("Do you want to play again? (yes/no): ").lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def get_player_type(player_char):
    while True:
        player_choice = input(f"Choose the type for Player {player_char} (human/random/smart): ").lower()
        if player_choice == 'human':
            return HumanPlayer(player_char)
        elif player_choice == 'random':
            return RandomComputerPlayer(player_char)
        elif player_choice == 'smart':
            return SmartComputerPlayer(player_char)
        else:
            print("Invalid choice. Please enter 'human', 'random', or 'smart'.")


def save_game(game, filename="tictactoe_save.json"):
    """Saves the current game state to a JSON file."""
    game_data = game.get_game_state()
    try:
        with open(filename, 'w') as f:
            json.dump(game_data, f)
        print(f"Game saved to {filename}")
        return True
    except IOError:
        print(f"Error saving game to {filename}")
        return False


def load_game(filename="tictactoe_save.json"):
    """Loads a game state from a JSON file."""
    try:
        with open(filename, 'r') as f:
            game_data = json.load(f)
        game = TicTacToe()
        game.load_game_state(game_data)
        print(f"Game loaded from {filename}")
        return game
    except FileNotFoundError:
        print(f"Save file {filename} not found. Starting a new game.")
        return TicTacToe()
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}. Starting a new game.")
        return TicTacToe()
    except IOError:
        print(f"Error reading file {filename}. Starting a new game.")
        return TicTacToe()


def display_game_history(history):
    """Displays a list of game outcomes."""
    if not history:
        print("No game history available.")
        return

    print("\n--- Game History ---")
    for i, result in enumerate(history):
        if result == 'X':
            print(f"Game {i+1}: X wins")
        elif result == 'O':
            print(f"Game {i+1}: O wins")
        else:
            print(f"Game {i+1}: Tie")


def play_multiple_games():
    x_wins = 0
    o_wins = 0
    ties = 0
    game_history = []

    while True:
        print("\n--- New Game ---")
        x_player = get_player_type('X')
        o_player = get_player_type('O')
        game = TicTacToe()

        # Option to load a saved game at the start of multiple games
        load_option = input("Load saved game? (yes/no): ").lower()
        if load_option in ['yes', 'y']:
            loaded_game = load_game()
            if loaded_game:
                game = loaded_game
                game.print_board()
                game.display_move_history()

        winner = play(game, x_player, o_player)
        game_history.append(winner)

        if winner == 'X':
            x_wins += 1
        elif winner == 'O':
            o_wins += 1
        else:
            ties += 1

        print(f"\n--- Game Results ---")
        print(f"X Wins: {x_wins}")
        print(f"O Wins: {o_wins}")
        print(f"Ties: {ties}")

        game.display_move_history()

        save_option = input("Save this game? (yes/no): ").lower()
        if save_option in ['yes', 'y']:
            save_game(game)

        if not play_again():
            break

    display_game_history(game_history)


if __name__ == '__main__':
    play_multiple_games()
 
