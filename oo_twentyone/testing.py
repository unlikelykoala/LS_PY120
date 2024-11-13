import random
import os
import time
TERM_SIZE = os.get_terminal_size()

def clear_screen():
    os.system('clear')

def print_terminal_line():
    print("-" * TERM_SIZE.columns)

def wait(seconds):
    time.sleep(seconds)

class Card:
    SUITS = ['♣','♡', '♠', '♢']
    RANKS = [str(num) for num in range(2, 11)] + ['J', 'Q', 'K', 'A']
    VALUES = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
        'A' : 11,
    }
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.suit}{self.rank}'

    def ascii_card(self):
        card_display = []
        symbol = self.suit
        num1 = self.rank
        num2 = ' ' if len(self.rank) != 2 else ''
        card_display.append("•---------•")
        card_display.append(f"| {num1}{num2}      |")
        card_display.append("|         |")
        card_display.append(f"|    {symbol}    |")
        card_display.append("|         |")
        card_display.append(f"|       {num1}{num2}|")
        card_display.append("•---------•")
        return card_display

    @property
    def value(self):
        return Card.VALUES[self.rank]

class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = [Card(suit, rank)
            for suit in Card.SUITS
            for rank in Card.RANKS
        ]
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        if not isinstance(card, Card):
            raise TypeError('Must be a card object to add to deck')
        self.cards.append(card)

    def show_all_cards(self):
        all_cards = []
        for card in self.cards:
            all_cards.append(card.ascii_card())

        for pieces in zip(*(card for card in all_cards)):
            print('   '.join(pieces))
        print(f'Total: {self.value}')

    def show_first_card(self):
        all_cards = []
        for card in self.cards[:1]:
            all_cards.append(card.ascii_card())

        for pieces in zip(*(card for card in all_cards)):
            print('   '.join(pieces))
        print(f'Total: {self.value - self.cards[1].value}')

    def is_busted(self):
        return self.value > 21

    def reset(self):
        self.cards = []

    @property
    def value(self):
        sum_val = 0

        for card in self.cards:
            sum_val += card.value

        for card in self.cards:
            if sum_val <= 21:
                break
            if card.rank == 'A':
                sum_val -= 10

        return sum_val

class Player:
    INITIAL_BANK = 5
    RICH_BANK = 2 * INITIAL_BANK

    def __init__(self):
        self.bank = Player.INITIAL_BANK
        self.hand = Hand()
        self.bank = Player.INITIAL_BANK

    def is_rich(self):
        return self.bank == Player.RICH_BANK

    def increase_bank(self):
        self.bank += 1

    def decrease_bank(self):
        self.bank -= 1


class Dealer:
    def __init__(self):
        self.hand = Hand()

    def show_first_card(self):
        self.hand.show_first_card()

class TwentyOneGame:
    HIT = 'h'
    STAY = 's'

    def __init__(self):
        self.deck = Deck()
        self.human = Player()
        self.dealer = Dealer()

    def start(self):
        self.display_welcome_message()

        while True:
            self.play_round()
            if self.human.bank == 0:
                break
            if self.human.is_rich():
                break
            if not self.play_again():
                break
            self.reset_hands()

        self.display_goodbye_message()

    def play_round(self):
        self.deal_cards()
        self.show_first_cards()
        self.player_turn()

        if not self.human.hand.is_busted():
            self.dealer_turn()

        self.display_result()
        self.update_bank()
        self.display_bank()
        wait(1)

    def reset_hands(self):
        self.human.hand.reset()
        self.dealer.hand.reset()

    def update_bank(self):
        winner = self.who_won()
        if winner == self.human:
            self.human.increase_bank()
        elif winner == self.dealer:
            self.human.decrease_bank()

    def display_bank(self):
        print(f"You have ${self.human.bank}!")

    def display_winnings(self):
        if self.human.bank < Player.INITIAL_BANK:
            print(f"You lost ${Player.INITIAL_BANK - self.human.bank}"
                  f" and ended with ${self.human.bank}.\n")
        elif self.human.bank > Player.INITIAL_BANK:
            print(f"You won ${self.human.bank - Player.INITIAL_BANK}"
                  f" and are walking away with ${self.human.bank}!\n")
        else:
            print(f"You didn't lose any money!"
                  f" You still have your ${self.human.bank} left! Nice job.\n")

    def deal_cards(self):
        for _ in range(2):
            self.human.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())

    def show_first_cards(self):
        clear_screen()
        self.dealer.show_first_card()
        print_terminal_line()
        self.human.hand.show_all_cards()

    def show_all_cards(self):
        clear_screen()
        self.dealer.hand.show_all_cards()
        print_terminal_line()
        self.human.hand.show_all_cards()

    def hit_or_stay(self):
        while True:
            answer = input("Would you like to hit or stay?"
                           " (h/s): ").strip().lower()
            if not answer:
                print("Invalid input, please type 'h' to hit or 's' to stay.")
                continue
            if answer[0] in TwentyOneGame.HIT:
                return True
            if answer[0] in TwentyOneGame.STAY:
                return False
            print("Invalid input, Try again.")

    def player_turn(self):
        while self.hit_or_stay():
            self.hit(self.human.hand)
            clear_screen()
            self.dealer.show_first_card()
            print_terminal_line()
            self.human.hand.show_all_cards()
            if self.human.hand.is_busted():
                break

    def hit(self, hand):
        hand.add_card(self.deck.deal())

    def stay(self):
        pass

    def dealer_turn(self):
        self.show_all_cards()
        while self.dealer.hand.value < 17:
            print('Dealer is thinking...')
            wait(1)
            self.hit(self.dealer.hand)
            self.show_all_cards()
            if self.dealer.hand.is_busted():
                break
        wait(1)

    def who_won(self):
        if self.human.hand.is_busted():
            return self.dealer
        if self.dealer.hand.is_busted():
            return self.human

        human_score = self.human.hand.value
        dealer_score = self.dealer.hand.value

        if human_score > dealer_score:
            return self.human
        if dealer_score > human_score:
            return self.dealer
        return None

    def display_result(self):
        if self.human.hand.is_busted():
            print("You Bust! Dealer Wins!")
        elif self.dealer.hand.is_busted():
            print("Dealer Busts! You win!")
        else:
            winner = self.who_won()
            if winner is self.dealer:
                print("Dealer wins!")
            elif winner is self.human:
                print("You win!")
            else:
                print("Push! Nobody wins.")

    def display_goodbye_message(self):
        clear_screen()
        self.display_winnings()
        print("Thanks for playing twenty-one!\n")

    def play_again(self):
        while True:
            answer = input('Would you like to play again?'
                           ' (y/n): ').strip().lower()
            if answer == '':
                print("Sorry that's not a valid input.")
                continue
            if answer[0] == 'y':
                return True
            if answer[0] == 'n':
                return False
            print("Sorry that's not a valid input.")

    def display_welcome_message(self):
        clear_screen()
        while True:
            answer = input("Welcome to twenty-one! Would you like"
            " to view the instructions? (y/n) \n").strip().lower()

            if answer == '':
                print("Invalid input. Please try again.")
                continue

            if answer[0] == 'y':
                self.display_instructions()
                break
            if answer[0] == 'n':
                break

            print("Invalid input. Please try again.")
            wait(1)

    @staticmethod
    def enter_to_continue():
        while True:
            answer = input("Please press 'enter' to continue...\n")
            if answer.strip() == '':
                break
            print("Invalid input. Try again")

    @staticmethod
    def display_instructions():
        clear_screen()
        print('Welcome To 21!\n')
        print("Get as close to 21 as possible without going over.")
        print("Each player starts with 2 cards."
              " One of the dealer's cards is hidden.")
        print("Options: 'Hit' to add cards to your total,"
              " 'Stay' to hold your total.")
        print("Going over 21 is a 'bust', resulting in an automatic loss.")
        print("Dealer hits until reaching 17 or higher.\n")
        print("Oh, and each bet is worth $1."
              f" You have a starting balance of ${Player.INITIAL_BANK}.")
        print("Try not to lose too much money! ;)")
        print("Good luck!\n")
        TwentyOneGame.enter_to_continue()

game = TwentyOneGame()
game.start()
