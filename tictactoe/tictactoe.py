import os
import random


class Square:
    INITIAL_MARKER = " "
    HUMAN_MARKER = "X"
    COMPUTER_MARKER = "O"
    
    def __init__(self, marker=INITIAL_MARKER):
        self.marker = marker

    @property
    def marker(self):
        return self._marker
    
    @marker.setter
    def marker(self, marker):
        self._marker = marker
    
    def is_unused(self):
        return self.marker == Square.INITIAL_MARKER
    
    def __str__(self):
        return self.marker

class Board:
    def __init__(self):
        self.squares = {key: Square() for key in range(1, 10)}

    def count_markers_for(self, player, keys):
        markers = [self.squares[key].marker for key in keys]
        return markers.count(player.marker)
    
    def display(self):
        print()
        print("     |     |")
        print(f"  {self.squares[1]}  |"
              f"  {self.squares[2]}  |"
              f"  {self.squares[3]}")
        print("     |     |")
        print("-----+-----+-----")
        print("     |     |")
        print(f"  {self.squares[4]}  |"
              f"  {self.squares[5]}  |"
              f"  {self.squares[6]}")
        print("     |     |")
        print("-----+-----+-----")
        print("     |     |")
        print(f"  {self.squares[7]}  |"
              f"  {self.squares[8]}  |"
              f"  {self.squares[9]}")
        print("     |     |")
        print()

    def is_full(self):
        return len(self.unused_squares()) == 0
    
    def mark_square_at(self, key, marker):
        self.squares[key].marker = marker

    def reset(self):
        self.squares = {key: Square() for key in range(1, 10)}

    def unused_squares(self):
        return [key
                for key, square in self.squares.items()
                if square.is_unused()]
    
    def is_unused_square(self, key):
        return self.squares[key].is_unused()

class Player:
    def __init__(self, marker):
        self.marker = marker
        self.wins = 0

    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, value):
        self._marker = value

class Human(Player):
    def __init__(self):
        super().__init__(Square.HUMAN_MARKER)

class Computer(Player):
    def __init__(self):
        super().__init__(Square.COMPUTER_MARKER)

class TTTGame:
    POSSIBLE_WINNING_ROWS = (
        (1, 2, 3),  # top row of board
        (4, 5, 6),  # center row of board
        (7, 8, 9),  # bottom row of board
        (1, 4, 7),  # left column of board
        (2, 5, 8),  # middle column of board
        (3, 6, 9),  # right column of board
        (1, 5, 9),  # diagonal: top-left to bottom-right
        (3, 5, 7),  # diagonal: top-right to bottom-left
    )
    
    def __init__(self):
        self.board = Board()
        self.human = Human()
        self.computer = Computer()

    def play(self):
        self.display_welcome_message()

        while True:
            self.play_one_game()
            if not self.play_again():
                break

        self.display_goodbye_message()

    def play_one_game(self):
        self.board.reset()
        self.board.display()

        while True:
            self.human_moves()
            if self.is_game_over():
                break

            self.computer_moves()
            if self.is_game_over():
                break

            self.board.display()

        self.board.display()
        self.display_results()

    
    def play_again(self):
        print('Do you want to play again?')
        response = input("Enter y/n: ")

        while not response.lower().startswith(('y', 'n')):
            print('Invalid input. Do you want to play again?')
            response = input("Enter y/n: ")

        return response.lower().startswith('y')

    
    def display_welcome_message(self):
        print("Welcome to Tic Tac Toe!")

    def display_goodbye_message(self):
        print("Thanks for playing Tic Tac Toe! Goodbye!")

    def display_results(self):
        if self.is_winner(self.human):
            print("You won! Congratulations!")
        elif self.is_winner(self.computer):
            print("I won! I won! Take that, human!")
        else:
            print("A tie game. How boring.")

    def is_winner(self, player):
        for row in TTTGame.POSSIBLE_WINNING_ROWS:
            if self.three_in_a_row(player, row):
                return True

        return False

    def human_moves(self):
        while True:
            valid_choices = self.board.unused_squares()
            choices_list = [str(choice) for choice in valid_choices]
            choices_str = TTTGame.join_or(choices_list)
            prompt = f"Choose a square ({choices_str}): "
            choice = input(prompt)

            try:
                choice = int(choice)
                if choice in valid_choices:
                    break
            except ValueError:
                pass

            print("Sorry, that's not a valid choice.")
            print()

        self.board.mark_square_at(choice, self.human.marker)

    def computer_moves(self):
        choice = self.offensive_move()

        if not choice:
            choice = self.defensive_move()

        if not choice:
            choice = self.center_move()

        if not choice:
            choice = self.random_move()

        self.board.mark_square_at(choice, self.computer.marker)

    def offensive_move(self):
        for row in TTTGame.POSSIBLE_WINNING_ROWS:
            key = self.winning_square(self.computer, row)
            if key:
                return key

        return None

    def defensive_computer_move(self):
        for row in TTTGame.POSSIBLE_WINNING_ROWS:
            key = self.winning_square(self.human, row)
            if key:
                return key

        return None

    def center_move(self):
        CENTER = 5 
        return CENTER if self.board.is_unused_square(CENTER) else None

    def random_move(self):
        valid_choices = self.board.unused_squares()
        return random.choice(valid_choices)

    def winning_square(self, player, row):
        if self.board.count_markers_for(player, row) == 2:
            for key in row:
                if self.board.is_unused_square(key):
                    return key

        return None

    @staticmethod
    def join_or(lst, delimiter=', ', last='or'):
        if len(lst) == 1:
            return str(lst[0])
        elif len(lst) == 2:
            return f'{lst[0]} {last} {lst[1]}'
        else:
            return f'{delimiter.join(lst[:-1])}{delimiter}{last} {lst[-1]}'

    def is_game_over(self):
        return self.board.is_full() or self.someone_won()

    def three_in_a_row(self, player, row):
        return self.board.count_markers_for(player, row) == 3

    def someone_won(self):
        return (self.is_winner(self.human) or
                self.is_winner(self.computer))


game = TTTGame()
game.play()
