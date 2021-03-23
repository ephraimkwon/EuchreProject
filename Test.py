from player import *
from cards import *
from game import *
import random as rand
# game = Game()
# game.set_up()
# game.play()

jack_of_spades = Card(2,0)
jack_of_clubs = Card(2,2)
jack_of_hearts = Card(2,1)
jack_of_diamonds = Card(2,3)


cards_in_play = [jack_of_diamonds,Card(0,1)]


trump_suit = 1

winning_card_index = -1

lead_suit = cards_in_play[0].suit


for index,card in enumerate(cards_in_play):
    print(winning_card_index)
    if winning_card_index < 0:
        winning_card_index = 0
    elif card.suit == cards_in_play[0].suit and card.value == 2 and card.suit % 2 == trump_suit % 2:
        continue
    elif card.suit == lead_suit:
        if card.value > cards_in_play[winning_card_index].value:
            winning_card_index = index
for index,card in enumerate(cards_in_play):
    if card.suit == trump_suit or (card.suit % 2 == trump_suit % 2 and card.value == 2):
        print(winning_card_index)
        if cards_in_play[winning_card_index].suit != trump_suit and not (cards_in_play[winning_card_index].value == 2 and cards_in_play[winning_card_index].suit % 2 == trump_suit):
            winning_card_index = index
        elif card.value == 2 and card.suit == trump_suit:
            winning_card_index = index
            break
        elif card.value == 2 and card.suit % 2 == trump_suit % 2:
            winning_card_index = index
        else:
            if card.value > cards_in_play[winning_card_index].value and cards_in_play[winning_card_index].value != 2:
                winning_card_index = index
winning_card = cards_in_play[winning_card_index]
print(winning_card_index)
print("This is the winning card!" , winning_card)