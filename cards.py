import random

class Card(object):
    def __init__(self, value, suit):
            self.value = value
            self.suit = suit
    def __repr__(self):
        value_name = ""
        suit_name = ""
        if self.value == 0:
            value_name = "Nine"
        elif self.value == 1:
            value_name = "Ten"
        elif self.value == 2:
            value_name = "Jack"
        elif self.value == 3:
            value_name = "Queen"
        elif self.value == 4:
            value_name = "King"
        elif self.value == 5:
            value_name = "Ace"
        if self.suit == 0:
            suit_name = "Spades"
        elif self.suit == 1:
            suit_name = "Hearts"
        elif self.suit == 2:
            suit_name = "Clubs"
        elif self.suit == 3:
            suit_name = "Diamonds"
        return value_name + " of " + suit_name

class Euchre_Deck(list):
    def __init__(self):
        super().__init__()
        suits = list(range(4))
        values = list(range(6))
        [[self.append(Card(value,suit)) for suit in suits] for value in values]
    def shuffle(self):
        random.shuffle(self)
    def deal(self,to_player):
        to_player.hand.append(self.pop(0))

deck = Euchre_Deck()

