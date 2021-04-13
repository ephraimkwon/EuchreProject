import socket
import threading
from game_online import Game
import time

game = Game()

host = socket.gethostbyname(socket.gethostname())

port = 5555

standard = "utf-8"

suit_dict = {0: "Spades", 1: "Hearts", 2: "Clubs", 3: "Diamonds"}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((host,port))
except Exception as e:
    print(e)

server.listen(4)

clients = []
names = []
messages = []

def broadcast(message):
    for client in clients:
        client.send(message)

# if message.decode('utf-8') == "eph: test":
#   clients[0].send(str.encode("Fuck"))

def handle(client):
    while True:
        try:
            if len(clients) == 5:
                broadcast(str.encode("Let's begin!\nSetting up players..."))
                game.set_up(names)
                game.deal_cards()
                
                for client in clients:
                    game_thread = threading.Thread(target = start_game, args = (client,))
                    game_thread.start()
                break
            elif len(clients) == 4:
                message = clients[0].recv(1024)
                if message.decode(standard) == f"{names[0]}: start":
                    clients[0].send(str.encode("Initialize everyone by pressing enter 3 times\nThen, enter your answer"))
                    broadcast(str.encode("Let's begin!\nSetting up players..\nCards have been dealt! Here is your top card:\n"))
                    game.set_up_test(names)
                    game.deal_cards()
                    start_game()
                break
            else:
                pass
        except Exception as e:
            print(e)
            index = clients.index(client)
            clients.remove(client)
            name = names[index]
            broadcast(f"{name} has left the game.".encode('utf-8'))
            names.remove(name)
            client.close()
            print(str(len(clients))+ "/4 players are in")
            break

player_list = [(),(),(),()]

def start_game():
    for i in range(len(player_list)):
        player_list[i] += (clients[i],names[i],game.player_list[i]) # a master list of all the important variables
    while not game.game_over:
        try:
            decide_trump_card()
            break
        except Exception as e:
            print(e)
            break

def decide_trump_card():
    game.set_dealer()
    set_order_deal(player_list)
    set_order_trick(player_list)
    broadcast(str.encode(f'{game.get_top_card()}'))
    for client, name, player in player_list:
        while True:
            client.send(str.encode(player.return_hand()))
            client.send(str.encode("Would you like to make top card trump? (Y/N)\n"))
            message = client.recv(1024)
            if message.decode("utf-8").lower() == f"{name}: y" or message.decode("utf-8").lower() == f"{name}: n":
                break
            else:
                client.send(str.encode("Please input either a y or n."))  
                continue
            break
        if message.decode('utf-8').lower() == f"{name}: y":
            broadcast(str.encode(f"{name} has chosen trump."))
            for client, name, player in player_list:
                print(player.is_dealer)
                if player.is_dealer:
                    client.send(str.encode(player.return_hand()))
                    while True:
                        try:
                            client.send(str.encode("Which card would you like to switch? (Input a number)\n"))
                            reply = client.recv(1024)
                            answer = reply.decode(standard)[-1]
                            switch_card = int(answer) - 1
                        except:
                            client.send(str.encode("Please input a number.\n"))
                            continue
                        if switch_card in range(5):
                            break
                        else:
                            client.send(str.encode("Please input a number.\n"))
                            continue
                    player.hand.append(game.deck[0])
                    player.called_trump = True
                    del player.hand[switch_card]
                    game.trump_suit = game.deck[0].suit
                    player.show_hand()
                    broadcast(str.encode(f"The trump suit is {suit_dict[game.deck[0].suit]}"))
                    break
            break
        elif message.decode(standard).lower() == f"{name}: n" and not player.is_dealer:
            continue
        elif message.decode(standard).lower() == f"{name}: n" and player.is_dealer:
            pass
            decide_trump_no_card()
        print("finished")
        break

def decide_trump_no_card():
    set_order_deal(player_list)
    broadcast(str.encode(f"The trump suit {suit_dict[game.deck[0].suit]} is now an invalid trump suit!"))
    for client, name, player in player_list:
        while True:
            client.send(str.encode(player.return_hand()))
            client.send(str.encode("Press enter, then answer.\n"))
            client.send(str.encode("Would you like to choose trump? (Y/N)\n"))
            message = client.recv(1024)
            if message.decode("utf-8").lower() in [f"{name}: y", f"{name}: n"]:
                break
            else:
                client.send(str.encode("Please input either y or n."))
                continue
            break
        if message.decode(standard).lower() == f"{name}: y":
            broadcast(str.encode(f"{name} has chosen trump!"))
            client.send(str.encode("Suits are:\n 1: Spades \n 2: Hearts \n 3: Clubs \n 4: Diamonds"))
            while True:
                try:
                    client.send(str.encode("What suit would you like to be trump?\n"))
                    reply = client.recv(1024)
                    answer = reply.decode(standard)[-1]
                    trump_num = int(answer) - 1
                except:
                    client.send(str.encode("Please input a number 1-4.\n"))
                    continue
                if trump_num == game.deck[0].suit:
                    client.send(str.encode("This is an invalid suit. Please chose a different suit.\n"))
                    continue
                elif trump_num not in range(4):
                    client.send(str.encode("Please input a number 1-4.\n"))
                    continue
                else:
                    break
            player.called_trump = True
            game.trump_suit = trump_num
            broadcast(str.encode(f"The trump suit is {suit_dict[trump_num]}!"))
            break
        if message.decode(standard).lower() == f"{name}: n" and not player.is_dealer:
            continue
        elif message.decode(standard).lower() == f"{name}: n" and player.is_dealer:
            client.send(str.encode("You just got screwed! You must choose the trump suit."))       
            client.send(str.encode("Suits are:\n 1: Spades \n 2: Hearts \n 3: Clubs \n 4: Diamonds"))
            while True:
                try:
                    client.send(str.encode("What suit would you like to be trump?\n"))
                    reply = client.recv(1024)
                    answer = reply.decode(standard)[-1]                    
                    trump_num = int(answer) - 1
                except:
                    client.send(str.encode("Please input a number 1-4.\n"))
                    continue
                if trump_num == game.deck[0].suit:
                    client.send(str.encode("This is an invalid suit. Please chose a different suit.\n"))
                    continue
                elif trump_num not in range(4):
                    client.send(str.encode("Please input a number 1-4.\n"))
                    continue
                else:
                    break
            player.called_trump = True
            game.trump_suit = trump_num
            broadcast(str.encode(f"The trump suit is {suit_dict[trump_num]}!"))
            break

def play_trick():
    set_order_deal()
    set_order_trick()
    game.reset_won_trick()
    for client, name, player in player_list:
        for player in game.player_list:
            valid_cards = [] # the indexes of the cards that can be put into play.
            for index, card in enumerate(player.hand):
                if len(game.cards_in_play) > 0: 
                    # This makes sure that if the leading card is the left bower, then only trumps are valid. 
                    if game.cards_in_play[0].value == 2 and game.cards_in_play[0].suit % 2 == game.trump_suit % 2 and game.cards_in_play[0].suit != game.trump_suit:
                        for index, card in enumerate(player.hand):
                            if card.suit == game.trump_suit:
                                valid_cards.append(index)
                        break
                    # This makes sure left bower is valid when the leading card is a trump suit card.
                    elif card.value == 2 and card.suit % 2 == game.trump_suit % 2 and game.cards_in_play[0].suit == game.trump_suit:
                        valid_cards.append(index)
                    # This checks that left bower is not valid if the leading card matches left bower suit.
                    elif card.suit == game.cards_in_play[0].suit and card.value == 2 and card.suit % 2 == game.trump_suit % 2:
                        continue
                    elif card.suit == game.cards_in_play[0].suit:
                        valid_cards.append(index)
                if len(game.cards_in_play) == 0:
                    valid_cards.append(index)
            for index, card in enumerate(player.hand):
                if len(valid_cards) == 0:
                    for i in range(len(player.hand)):
                        valid_cards.append(i)

def set_order_deal(player_list):
    for client, name, player in player_list:
        if player.is_dealer == True:
            for i in range(1, 5):
                if player.original_seat_num == i:
                    player.seat_num = 4
                    for client, name, other in player_list:
                        if other.original_seat_num != i:
                            other.seat_num = other.original_seat_num
                            if i != 4: 
                                other.seat_num -= i
                                other.seat_num %= 4 #loop back to remain 1-4 and not get a negative number
    player_list.sort(key = lambda x: x[2].seat_num, reverse = False)

def set_order_trick(player_list):
    for client, name, player in player_list:
        if player.won_trick == True:
            if player.original_seat_num == 4:
                player.seat_num = 1
                for client, name, player in player_list:
                    if player.original_seat_num != 4:
                        player.seat_num = player.original_seat_num
    player_list.sort(key = lambda x: x[2].seat_num, reverse = False)

def receive():
    while len(clients) < 5:
        conn, address = server.accept()
        print("Connected to ", address)
        conn.send(str.encode("NAME"))
        name = conn.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(conn)
        broadcast(f"{name} has joined the game!".encode('utf-8'))
        print(str(len(clients))+ "/4 players are in")

        conn.send(f"Connected to server\n You are player {len(clients)}".encode("utf-8"))
        if len(clients) == 4:
            broadcast(str.encode("Chatting over! Time to start the game."))
        thread = threading.Thread(target = handle, args = (conn,))
        thread.start()
print("Server started. Waiting for connections...")

receive()