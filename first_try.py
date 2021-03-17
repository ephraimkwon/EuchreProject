from enum import Enum
from enum import IntEnum
import random as random

class Player:
    def __init__(self, name):
        self.name = name
        self.team = 0
        self.hand = []
        self.tricks = 0
    def setTeam(self, num):
        self.team = num
    def playCard(self, index):
        return self.hand.pop(index)

class Deck():
    def __init__(self, deck = []):
        self.deck = deck
    def dealCards(self, Player_list):
        count = 0
        self.deck = random.sample(self.deck, len(self.deck))
        for player in Player_list:
            player.hand = self.deck[count:count+5]
            player.hand = enumerate(player.hand)
            count += 5
        self.deck = self.deck[20:]

    def getDeck(self):
        return self.deck
    
    def getTopCard(self):
        return drawCard(self.deck)

class Game:
    def __init__(self, deck_object, player_list = []):
        self.deck = deck_object
        self.player_list = player_list
        self.cards_in_play = []


class PlayingCard:
    def __init__(self, card_number, card_suit):
        self.card = card_number
        self.suit = card_suit
    def __str__(self):
        return f"{self.card.name} of {self.suit.name}"
    def __eq__(self, card):
        return self.card.name == card.card.name and self.suit.name == card.suit.name
    

class Suit(Enum):
    SPADES = 'spades'
    CLUBS = 'clubs'
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'

class Number(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

def createEuchreDeck():
    deck = []
    for num in Number:
        for suit in Suit:
            deck.append(PlayingCard(Number(num),Suit(suit)))
    euchre_deck = deck[28:len(deck)]
    return euchre_deck

def drawCard(deck):
    rand_card = random.randint(0, len(deck)-1)
    return deck.pop(rand_card)