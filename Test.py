from player import *
from cards import *
from game import *

game = Game()
game.set_up()
game.deal_cards()

game.decide_trump_top_card()
for i in range(5):
    game.play_trick()
    game.score_round()
    print(game.cards_in_play)
    print(game.team_1)
    print(game.team_2)
