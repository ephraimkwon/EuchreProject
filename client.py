from game import *
from player import *
from cards import *
from network import Network

def main():
    run = True
    n = Network()
    game = Game()
    name = input("Input a name \n")
    player = Player(name)
    n.send(name)

main()