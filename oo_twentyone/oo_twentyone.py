import os
import random
import sys
import time


def clear_terminal():
    os.system('clear')

def enter_to_clear(message="(Press 'Enter' to continue)"):
    input(message)
    transition()

def enter_to_continue(message="(Press 'Enter' to continue)"):
    input(message)
    print("\033[F\033[K", end='')
    flush_print()
    pause()

def pause(seconds=0.3):
    time.sleep(seconds)

def transition(seconds=0.3):
    clear_terminal()
    pause(seconds)

def flush_print():
    sys.stdout.flush()

def join_and(lst):
    lst = [str(ele) for ele in lst]
    if len(lst) == 1:
        return f'{lst[0]}.'
    if len(lst) == 2:
        return f'{lst[0]} and {lst[1]}.'

    return ', '.join(lst[:-1]) + f', and {lst[-1]}.'

class Card:
    RANKS_AND_POINTS = ({str(i):i for i in range(2,11)} |
    {'jack': 10, 'queen': 10, 'king': 10, 'ace': 11})
    SUITS = {'hearts', 'clubs', 'spades', 'diamonds'}

    def __init__(self, suit, rank, points):
        self.rank = rank
        self.suit = suit
        self.points = points

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank):
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, suit):
        self._suit = suit

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    def __str__(self):
        if self.rank.startswith(('8', 'a')):
            return f'an {self.rank} of {self.suit}'

        return f'a {self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards = self._generate_deck()

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards):
        self._cards = cards

    def deal_1_card(self):
        if not self.cards:
            self.cards = self._generate_deck()

        return self.cards.pop()

    def _generate_deck(self):
        new_deck = [Card(suit, rank, points) for suit in Card.SUITS
                        for rank, points in Card.RANKS_AND_POINTS.items()]
        random.shuffle(new_deck)
        return new_deck

class Participant:
    def __init__(self):
        self.hand = []
        self.dollars = 5

    def add_card(self, card):
        self.hand.append(card)

    def discard_hand(self):
        self.hand.clear()

    def decrement_dollars(self, loss=1):
        self.dollars -= loss

    def increment_dollars(self, gain=1):
        self.dollars += gain

    def display_dollars(self):
        print(f'You have ${self.dollars}.')
        print()
        enter_to_clear()

    def is_busted(self):
        return self.points() > TwentyOneGame.MAX_SCORE

    def points(self):
        points = 0
        aces = 0

        for card in self.hand:
            points += card.points
            if card.rank == 'ace':
                aces += 1

        while points > TwentyOneGame.MAX_SCORE and aces:
            points -= 10
            aces -= 1

        return points

class Player(Participant):
    STARTING_PURSE = 5
    WIN_PURSE = 10
    LOSE_PURSE = 0

    def __init__(self):
        super().__init__()
        self.dollars = Player.STARTING_PURSE

    @property
    def dollars(self):
        return self._dollars

    @dollars.setter
    def dollars(self, new):
        self._dollars = new

    def is_broke(self):
        return self.dollars == Player.LOSE_PURSE

    def is_rich(self):
        return self.dollars == Player.WIN_PURSE

    def bust(self):
        print('Oh no! You busted!')
        print()
        enter_to_clear()

    def show_hand(self):
        print('You have: ', end='')
        print(join_and(self.hand))
        print()
        pause()

    def show_new_card(self):
        print(f'You drew {self.hand[-1]}!')
        print()
        pause()

    def show_points(self):
        points = self.points()

        print(f'You have {points} points.')
        print()
        pause()

    def stay_message(self):
        print()
        print('You decided to stay.')
        print('Now it\'s the dealer\'s turn.')
        print()
        enter_to_clear()

class Dealer(Participant):
    STAY_SCORE = 17

    def bust(self):
        print('The dealer busted!')
        print()
        enter_to_clear()

    def hit_message(self):
        print('The dealer hits.')
        print()
        enter_to_clear()

    def stay(self):
        return self.points() > Dealer.STAY_SCORE

    def stay_message(self):
        print('The dealer stays.')
        print()
        enter_to_clear()

    def show_hand(self):
        print('The dealer has: ', end='')
        print(join_and(self.hand))
        print()
        pause()

    def show_hidden_hand(self):
        print('The dealer has: ', end='')
        hidden_cards = len(self.hand) - 1
        if hidden_cards == 1:
            print(f'{self.hand[0]} and {hidden_cards} hidden card.')
        else:
            print(f'{self.hand[0]} and {hidden_cards} hidden cards.')
        print()
        pause()

    def show_new_card(self):
        if len(self.hand) > 2:
            print(f'The dealer drew {self.hand[-1]}.')
            print()
            pause()

    def show_points(self):
        points = self.points()

        print(f'The dealer has {points} points.')
        print()
        pause()

class Rules:
    CARD_VALUES = [
        "- All number cards are worth their face values.\n\
    - e.g., a 2 of clubs is worth 2 points.",
    "- Jacks, Queens, and Kings are worth 10 points.",
    "- Aces can be either 1 point or 11 points.\n\
    - If a player has 10 or fewer points, an Ace is 11 points.\n\
    - If a player 11 or more points, an Ace is 1 point."
    ]

    GAME_RULES = [
    "The Goal: get your cards' total value as close to 21 \
as possible without going over.\n\
    - You can have a score of 21 exactly.\n\
    - If you go over 21, you bust (lose).",
    '1. Both you and the dealer are dealt two cards.\n\
    - You can look at both of your cards as well one of the dealer\'s.',
    '2. Your turn: decide if you want to hit (receive another card) \
or stay (end your turn).',
    "3. Dealer's turn: the dealer decides to hit or stay.\n\
    - The dealer must hit until their score is at least 17.\n\
    - If the dealer goes over 21, they bust, which means you win!",
    "4. If both you and the dealer stay, then you compare hands.\n\
    - The highest score wins.",
]

    GAMBLING_RULES = [
        '1. You will start with $5.',
        '2. If you win a round, you get $1. If you lose, you lose $1.',
        '3. The match is over when you have either $0 (lose) or $10 (win).'
    ]

    @staticmethod
    def continue_or_start():
        while True:
            response = input("Press Enter to continue or \
enter 'S' to start the game:  ")
            print("\033[F\033[K", end='')
            flush_print()
            pause()

            if response.casefold().startswith(('s', 'start')):
                return 'start'

            if not response:
                return 'continue'

            print("\033[F\033[K", end='')
            flush_print()
            pause()
            print('Invalid Input. Try again.')
            print()

    @classmethod
    def display_all_rules(cls):
        response = cls.display_game_rules()
        transition()
        if response == 'start':
            return None

        response = cls.display_card_values()
        transition()
        if response == 'start':
            return None

        cls.display_gambling_rules()
        return None

    @classmethod
    def display_card_values(cls):
        print('The card values are as follows: ')
        for rule in cls.CARD_VALUES:
            print()
            response = cls.continue_or_start()
            if response == 'start':
                return 'start'
            print(rule)

        print()
        response = cls.continue_or_start()
        if response == 'start':
            return 'start'

        return 'continue'

    @classmethod
    def display_game_rules(cls):
        print('The rules are simple:')
        for rule in cls.GAME_RULES:
            print()
            response = cls.continue_or_start()
            if response == 'start':
                return 'start'
            print(rule)

        print()
        response = cls.continue_or_start()
        if response == 'start':
            return 'start'

        return 'continue'

    @classmethod
    def display_gambling_rules(cls):
        print('Let\'s make it interesting:')
        for rule in cls.GAMBLING_RULES:
            print()
            response = cls.continue_or_start()
            if response == 'start':
                return None
            print(rule)

        print()
        enter_to_clear(message="Press 'Enter' to start the game)")
        return None

class TwentyOneGame:
    MAX_SCORE = 21

    def __init__(self):
        self._deck = Deck()
        self._player = Player()
        self._dealer = Dealer()

    def play(self):
        self.intro()

        while not self.match_over():
            self.play_round()

            if not self.play_again():
                break

        self.outro()

    def intro(self):
        self.display_welcome_message()

        if self.user_wants_rules():
            Rules.display_all_rules()

    def outro(self):
        self.display_match_result()
        self.display_goodbye_message()

    def deal_cards(self):
        for _ in range(2):
            self._player.add_card(self._deck.deal_1_card())
            self._dealer.add_card(self._deck.deal_1_card())

    def show_cards(self):
        self._dealer.show_hand()
        self._player.show_hand()

    def show_cards_hidden(self):
        self._dealer.show_hidden_hand()
        self._player.show_hand()

    def user_wants_rules(self):
        while True:
            print('Would you like to see the rules?')
            response = input("Enter 'y' for yes or 'n' for no: ")

            if response.casefold() in ['y', 'n']:
                transition()
                return response.casefold() == 'y'

            transition()
            print('Invalid response. Try again.')
            print()

    def _player_turn(self):
        while True:
            self.show_cards_hidden()

            self._player.show_points()

            if self._player.is_busted():
                self._player.bust()
                break

            if self._hit_or_stay() == 'stay':
                self._player.stay_message()
                break

            transition()
            self._hit(self._player)
            self._player.show_new_card()

    def _dealer_turn(self):
        while True:
            self._dealer.show_new_card()
            self._dealer.show_hand()

            if self._dealer.is_busted():
                self._dealer.bust()
                break

            if self._dealer.stay():
                self._dealer.stay_message()
                break

            self._hit(self._dealer)
            self._dealer.hit_message()

    def _update_dollars(self):
        winner = self._get_winner()

        if winner == self._player:
            self._player.increment_dollars()
        elif winner == self._dealer:
            self._player.decrement_dollars()

    def _compare_hands(self):
        if self._player.points() > self._dealer.points():
            return self._player
        if self._player.points() < self._dealer.points():
            return self._dealer

        return 'tie'

    def discard_hands(self):
        self._player.discard_hand()
        self._dealer.discard_hand()

    def display_welcome_message(self):
        transition()
        print('Welcome to Object-Oriented Twenty-One!')
        print()
        enter_to_clear()

    def display_goodbye_message(self):
        print('See you next time!')
        print()

    def display_match_result(self):
        if not self.match_over():
            return
        if self._player.is_broke():
            print('Sorry, you have $0. You\'re broke!')
            print()
            pause()
            print('Please leave our establishment.')
            print()
            pause()
        else:
            print('You have $10. You\'re rich!')
            print()
            pause()

    def display_result(self):
        self.display_winner()

        self._dealer.show_hand()
        self._dealer.show_points()

        self._player.show_hand()
        self._player.show_points()

        enter_to_clear()

    def display_winner(self):
        winner = self._get_winner()

        if winner == 'tie':
            print('It\'s a tie!')
        elif winner == self._player:
            print('You won!')
        else:
            print('The dealer won!')

        print()
        pause()

    def _get_winner(self):
        if self._player.is_busted():
            return self._dealer
        if self._dealer.is_busted():
            return self._player

        return self._compare_hands()

    def _hit(self, participant):
        card = self._deck.deal_1_card()
        participant.add_card(card)

    def _hit_or_stay(self):
        while True:
            print('Would you like to hit or stay?')
            response = input("Enter 'h' for hit or 's' for stay: ")

            match response.casefold():
                case 'h':
                    return 'hit'
                case 's':
                    return 'stay'
                case _:
                    transition()
                    print('Invalid input. Try again.')
                    print()
                    self.show_cards()
                    self._player.show_points()

    def match_over(self):
        return self._player.is_broke() or self._player.is_rich()

    def play_round(self):
        self.discard_hands()

        self.deal_cards()

        self._player_turn()
        if not self._player.is_busted():
            self._dealer_turn()

        self.display_result()
        self._update_dollars()
        self._player.display_dollars()

    def play_again(self):
        while True:
            print('Would you like to play again?')
            response = input("Enter 'y' for yes or 'n' for no: ")

            if response.casefold() in ['y', 'n']:
                transition()
                return response.casefold() == 'y'

            transition()
            print('Invalid response. Try again.')
            print()



game = TwentyOneGame()
game.play()
