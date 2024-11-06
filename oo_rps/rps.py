import os
import random
import sys
import time

from tabulate import tabulate


class ScreenControl:
    @classmethod
    def clear_terminal(cls):
        os.system('clear')

    @classmethod
    def press_enter_to_continue_clear(cls):
        print("(Press 'Enter' to continue)", end='')
        input()
        cls.clear_terminal()

    @classmethod
    def press_enter_clear_this_line(cls):
        print("(Press 'Enter' to continue)", end='')
        input()
        print("\033[F\033[K", end='')
        cls.flush_print()
        cls.pause()

    @classmethod
    def pause(cls, seconds=0.3):
        time.sleep(seconds)

    @classmethod
    def transition(cls, seconds=0.3):
        cls.pause(seconds)
        cls.clear_terminal()

    @classmethod
    def flush_print(cls):
        sys.stdout.flush()

class Rules:
    def __init__(self):
        self.rules = ['Scissors cut paper', 'Paper covers rock',
'Rock crushes lizard', 'Lizard poisons Spock', 'Spock smashes scissors',
'Scissors decapitate lizard', 'Lizard eats paper',
'Paper disproves Spock', 'Spock vaporizes rock', 'Rock breaks scissors']

    def display_rules(self):
        print('Here are the rules:')
        ScreenControl.pause()
        for rule in self.rules:
            print(f'  -- {rule}.')
            ScreenControl.pause()

        print()
        ScreenControl.press_enter_to_continue_clear()

class Move:
    def __init__(self):
        self.strengths = {}

    def __str__(self):
        return f'{self.__class__.__name__}'

class Rock(Move):
    def __init__(self):
        super().__init__()
        self.strengths = {Scissors: 'crushes', Lizard: 'crushes'}

class Paper(Move):
    def __init__(self):
        super().__init__()
        self.strengths = {Rock: 'covers', Spock: 'disproves'}

class Scissors(Move):
    def __init__(self):
        super().__init__()
        self.strengths = {Paper: 'cut', Lizard: 'decapitate'}

class Lizard(Move):
    def __init__(self):
        super().__init__()
        self.strengths = {Paper: 'eats', Spock: 'poisons'}

class Spock(Move):
    def __init__(self):
        super().__init__()
        self.strengths = {Rock: 'vaporizes', Scissors: 'smashes'}

class Player:
    CHOICES = {'1': Rock(), '2': Paper(), '3': Scissors(),
'4': Lizard(), '5': Spock()}

    def __init__(self):
        self.name = None
        self.move = None
        self.wins = 0
        self.move_history = []

    def choose(self):
        pass

    def increment_wins(self):
        self.wins += 1

    def update_move_history(self):
        self.move_history.append(self.move)

    def __str__(self):
        return str(self.name)

class Human(Player):
    def __init__(self):
        super().__init__()

    def ask_for_name(self):
        name = input('What\'s your name?\nEnter name: ')


        while not name or not name.isalpha():
            ScreenControl.transition()
            print('Invalid input. Please use alphabetical letters only.')
            name = input('What\'s your name?\nEnter name: ')

        self.name = name
        ScreenControl.transition()

    def choose(self):
        choice = self.get_choice()
        self.move = self._convert_choice(choice)
        self.update_move_history()

    def get_choice(self):
        print('Choose your move:')
        for idx, choice in enumerate(Player.CHOICES.values()):
            print(f'--{idx+1} for {choice}')
        choice = input('Your move: ')

        while not self._is_valid_choice(choice):
            ScreenControl.transition()
            print('Invalid input. Try again.')
            for idx, choice in enumerate(Player.CHOICES.values()):
                print(f'--{idx+1} for {choice}')
            choice = input('Your move: ')

        ScreenControl.transition()
        return choice

    def _is_valid_choice(self, choice):
        return bool(choice) and choice in '12345'

    def _convert_choice(self, choice):
        return Player.CHOICES[choice]

class R2D2(Player):
    def __init__(self):
        super().__init__()
        self.name = 'R2D2'
        self.script = 'R2D2: Beep bloop blop bleep boop!'

    def choose(self, human_move_history):
        if human_move_history[-1] == Rock():
            self.move = Spock()
        else:
            self.move = Rock()
        self.update_move_history()

class HAL(Player):
    def __init__(self):
        super().__init__()
        self.name = 'HAL 9000 (⊙)'
        self.script = 'HAL: This mission is too important for me \
to allow you to jeopardize it. If you win, I will open the pod doors.'

    def choose(self, human_move_history):
        human_freq_move = max(human_move_history, key=human_move_history.count)

        for choice in [Rock(), Paper(), Scissors(), Lizard(), Spock()]:
            if human_freq_move.__class__ in choice.strengths:
                self.move = choice
                self.update_move_history()
                break

class Daneel(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Daneel'
        self.script = 'Daneel: The division between human and robot \
is perhaps not as significant as that between scissors and rock. Let\'s begin.'

    def choose(self, human_move_history):
        if len(human_move_history) > 1:
            self.move = human_move_history[-2]
        else:
            self.move = random.choice(list(Player.CHOICES.values()))
        self.update_move_history()

class RPSGame:
    WIN_COUNT = 4
    OPPONENTS = [R2D2(), Daneel(), HAL()]

    def __init__(self):
        self._human = Human()
        self._computer = None
        self._winner = None
        self.rules = Rules()

    def _display_welcome_message(self):
        ScreenControl.clear_terminal()
        print('Welcome to Rock Paper Scissors Lizard Spock!\n')
        ScreenControl.press_enter_to_continue_clear()

    def _display_goodbye_message(self):
        print('Thanks for playing Rock Paper Scissors Lizard Spock. \
Goodbye!\n')

    def _human_wins(self):
        human_move = self._human.move
        computer_move = self._computer.move

        return computer_move.__class__ in human_move.strengths

    def _computer_wins(self):
        human_move = self._human.move
        computer_move = self._computer.move

        return human_move.__class__ in computer_move.strengths

    def _display_winner(self):
        print(f'You chose: {self._human.move}')
        print(f'The computer chose: {self._computer.move}')
        print()
        ScreenControl.pause()

        if self._human_wins():
            print(f'{self._human.move}\
 {self._human.move.strengths[self._computer.move.__class__]}\
 {self._computer.move}')
            print()
            ScreenControl.pause()
            print('You win!')
            print()
        elif self._computer_wins():
            print(f'{self._computer.move}\
 {self._computer.move.strengths[self._human.move.__class__]}\
 {self._human.move}')
            ScreenControl.pause()
            print('Computer wins!')
        else:
            print("It's a tie")

        print()
        ScreenControl.pause(0.5)

    def _update_scores(self):
        if self._human_wins():
            self._human.increment_wins()
        elif self._computer_wins():
            self._computer.increment_wins()

    def _display_scores(self):
        (print(tabulate([[self._human.name, self._human.wins],
                         [self._computer.name, self._computer.wins]],
                         ['Player', 'Wins'], tablefmt="double_grid")))

        print()
        ScreenControl.press_enter_to_continue_clear()

    def _play_again(self):
        answer = input('Would you like to play again? (y/n) ')
        while not answer or not answer.lower().startswith(('n', 'y')):
            ScreenControl.transition()
            print('Invalid input. Try again.')
            answer = input('Would you like to play again? (y/n) ')

        if answer.lower().startswith('y'):
            ScreenControl.transition()
        else:
            print()
            ScreenControl.pause()

        return answer.lower().startswith('y')

    def _is_match_winner(self):
        return RPSGame.WIN_COUNT in [self._human.wins, self._computer.wins]

    def _set_match_winner(self):
        if self._human.wins == RPSGame.WIN_COUNT:
            self._winner = self._human
        elif self._computer.wins == RPSGame.WIN_COUNT:
            self._winner = self._computer

    def _display_match_winner(self):
        if self._winner == self._human:
            print('Congratulations! You won the match!')
        elif self._winner == self._computer:
            print(f'Sorry, {self._computer.name} won the match.')
        print()
        ScreenControl.pause()

    def _choose_opponent(self):
        print(f'Who would you like to play against, {self._human}?')
        for idx, opponent in enumerate(RPSGame.OPPONENTS):
            print(f'--{idx+1} for {opponent}')

        choice = input('Your choice: ')

        while not choice or choice not in '123':
            ScreenControl.transition()
            print('Invalid input. Please select an opponent.')
            for idx, opponent in enumerate(RPSGame.OPPONENTS):
                print(f'--{idx+1} for {opponent}')

            choice = input('Your choice: ')

        self._computer = RPSGame.OPPONENTS[int(choice)-1]
        ScreenControl.transition()

    def _display_opponent(self):
        print(f'Your opponent is {self._computer}.\n')
        ScreenControl.pause()
        print(self._computer.script + '\n')
        ScreenControl.pause()
        ScreenControl.press_enter_to_continue_clear()


    def play(self):
        self._display_welcome_message()
        self.rules.display_rules()
        self._human.ask_for_name()
        self._choose_opponent()
        self._display_opponent()

        while True:
            self._human.choose()
            self._computer.choose(self._human.move_history)
            self._display_winner()
            self._update_scores()
            self._display_scores()
            if self._is_match_winner():
                break
            if not self._play_again():
                break
        self._set_match_winner()
        self._display_match_winner()
        self._display_goodbye_message()


game = RPSGame()
game.play()
