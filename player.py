"""
Tic-Tac-Toe players using inheritance implementation by Kylie YIng
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
import random


class Player():
    """Base class for a player."""
    def __init__(self, letter: str):
        """
        Initializes a Player instance.

        Args:
            letter (str): The identifier for the player.
        """
        if not isinstance(letter, str) or len(letter) != 1:
            raise ValueError("Player letter must be a single character string.")
        self.letter = letter

    def get_move(self, game):
        """
        Determines and returns the player's move in the given game.

        Args:
            game: The current game state or object.

        Returns:
            The player's chosen move. The specific type depends on the game.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the get_move method.")


class HumanPlayer(Player):
    """Represents a human player."""
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
    """Represents a computer player making random moves."""
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class SmartComputerPlayer(Player):
    """Represents a computer player using the minimax algorithm."""
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # Base cases: check for winner or tie
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Maximize score
        else:
            best = {'position': None, 'score': math.inf}  # Minimize score

        for possible_move in state.available_moves():
            state.make_move(possible_move, player, record=False)  # Simulate move
            sim_score = self.minimax(state, other_player)  # Recursive call

            # Undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class TicTacToe():
    """Represents the Tic Tac Toe game."""
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None
        self.move_history = []  # Keep track of moves made

    def make_board(self):
        return [' '] * 9

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter, record=True):
        if self.board[square] == ' ':
            self.board[square] = letter
            if record:
                self.move_history.append((square, letter))
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def undo_move(self):
        if self.move_history:
            last_move, last_letter = self.move_history.pop()
            self.board[last_move] = ' '
            self.current_winner = None

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

    def get_board_copy(self):
        return self.board[:]

    def is_full(self):
        return ' ' not in self.board

    def get_winning_combinations(self):
        return [
            self.board[0:3], self.board[3:6], self.board[6:9],  # Rows
            [self.board[i] for i in [0, 3, 6]], [self.board[i] for i in [1, 4, 7]], [self.board[i] for i in [2, 5, 8]],  # Columns
            [self.board[i] for i in [0, 4, 8]], [self.board[i] for i in [2, 4, 6]]  # Diagonals
        ]

    def check_win(self, letter):
        for combo in self.get_winning_combinations():
            if all(spot == letter for spot in combo):
                return True
        return False

    def get_potential_winning_moves(self, letter):
        winning_moves = []
        for move in self.available_moves():
            temp_board = self.get_board_copy()
            temp_board[move] = letter
            temp_game = TicTacToe()
            temp_game.board = temp_board
            if temp_game.check_win(letter):
                winning_moves.append(move)
        return winning_moves

    def get_potential_blocking_moves(self, letter):
        opponent_letter = 'O' if letter == 'X' else 'X'
        return self.get_potential_winning_moves(opponent_letter)

    def evaluate_board(self, maximizing_player):
        if self.check_win(maximizing_player.letter):
            return 1
        elif self.check_win('O' if maximizing_player.letter == 'X' else 'X'):
            return -1
        elif self.is_full():
            return 0
        else:
            return 0

    def get_empty_board_indices(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def get_occupied_board_indices(self):
        occupied = {'X': [], 'O': []}
        for i, spot in enumerate(self.board):
            if spot == 'X':
                occupied['X'].append(i)
            elif spot == 'O':
                occupied['O'].append(i)
        return occupied

    def print_move_history(self):
        if not self.move_history:
            print("No moves have been made yet.")
        else:
            print("Move History:")
            for move, letter in self.move_history:
                print(f"Player {letter} moved to square {move}")

    def check_future_win(self, letter, depth=2):
        if depth == 0:
            return False

        for move in self.available_moves():
            temp_board = self.get_board_copy()
            temp_board[move] = letter
            temp_game = TicTacToe()
            temp_game.board = temp_board
            if temp_game.check_win(letter):
                return True
            opponent_letter = 'O' if letter == 'X' else 'X'
            can_opponent_block_future_win = False
            for opponent_move in temp_game.available_moves():
                temp_board_opponent = temp_game.get_board_copy()
                temp_board_opponent[opponent_move] = opponent_letter
                temp_game_opponent = TicTacToe()
                temp_game_opponent.board = temp_board_opponent
                if temp_game_opponent.get_potential_winning_moves(letter):
                    can_opponent_block_future_win = True
                    break
            if not can_opponent_block_future_win and temp_game.empty_squares():
                return temp_game.check_future_win(letter, depth - 1)
        return False


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while True:
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(f"{letter} makes a move to square {square}")
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter

            if not game.empty_squares():
                if print_game:
                    print("It's a tie!")
                return None

            letter = 'O' if letter == 'X' else 'X'
        else:
            if isinstance(x_player, HumanPlayer) and letter == 'X' or isinstance(o_player, HumanPlayer) and letter == 'O':
                print('That square is already taken. Try again.')


if __name__ == '__main__':
    x_wins = 0
    o_wins = 0
    ties = 0
    num_games = 1
    for _ in range(num_games):
        x_player = SmartComputerPlayer('X')
        o_player = HumanPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=True)
        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1

    print(f'After {num_games} games, X won {x_wins} times, O won {o_wins} times, and there were {ties} ties')

    # Example of using the new functions:
    game = TicTacToe()
    game.make_move(0, 'X')
    game.make_move(4, 'O')
    print("\nExample using new functions:")
    print("Current board:")
    game.print_board()
    board_copy = game.get_board_copy()
    print("Copy of the board:", board_copy)
    print("Is the board full?", game.is_full())
    print("Winning combinations:", game.get_winning_combinations())
    print("Does X win?", game.check_win('X'))
    print("Does O win?", game.check_win('O'))
    print("Potential winning moves for X:", game.get_potential_winning_moves('X'))
    print("Potential blocking moves for X:", game.get_potential_blocking_moves('X'))
    print("Empty board indices:", game.get_empty_board_indices())
    print("Occupied board indices:", game.get_occupied_board_indices())
    game.print_move_history()
    print("Can X win in the next 2 moves?", game.check_future_win('X', depth=2))
 
