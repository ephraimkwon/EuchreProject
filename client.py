from game import *
from player import *
from cards import *
from network import Network

def main():
    while True:
        n = Network()
        name = input("Input your name \n")
        n.send(name)
        reply = n.listen()

main()
    