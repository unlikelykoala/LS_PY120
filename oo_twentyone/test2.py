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
    elif len(lst) == 2:
        return f'{lst[0]} and {lst[1]}.'
    else:
        return ', '.join(lst[:-1]) + f', and {lst[-1]}.'

class Card:
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
        else:
            return f'a {self.rank} of {self.suit}'

class Deck:
    RANKS_AND_POINTS = {str(i):i for i in range(2,11)} | {'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}
    SUITS = {'hearts', 'clubs', 'spades', 'diamonds'}
    
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
        new_deck = [Card(suit, rank, points) for suit in Deck.SUITS
                                              for rank, points in Deck.RANKS_AND_POINTS.items()]
        random.shuffle(new_deck)
        return new_deck

class Participant:
    def __init__(self):
        self.hand = []
        self.dollars = 5
    
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
        return self.points() > 21

    def points(self):
        points = 0
        aces = 0

        for card in self.hand:
            print(type(card.points))
            # points += card.points
            if card.rank == 'ace':
                aces += 1
        
        while points > 21 and aces:
            points -= 10
            aces -= 1

        return points

deck = Deck()

player = Participant()

player.hand.append(deck.deal_1_card())
player.hand.append(deck.deal_1_card())
player.hand.append(deck.deal_1_card())
player.hand.append(deck.deal_1_card())

player.points()
