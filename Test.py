from player import *
from cards import *
from game import *

game = Game()
game.set_up()
game.deal_cards()

game.play_full_round()
