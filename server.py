import socket
import threading
from game_online import Game
import time

game = Game()

host = socket.gethostbyname(socket.gethostname())

port = 5555

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
            message = client.recv(1024)
            if len(clients) == 5:
                broadcast(str.encode("Let's begin!\nSetting up players..."))
                game.set_up(names)
                game.deal_cards()
                
                for client in clients:
                    game_thread = threading.Thread(target = start_game, args = (client,))
                    game_thread.start()
                break
                
            elif message.decode('utf-8') == "a: test":
                print("Interesting")
                broadcast(str.encode("Let's begin!\nSetting up players..\nCards have been dealt! Here is your top card:\n"))
                game.set_up_test(names)
                game.deal_cards()
                start_game()
                
                # for client in clients:
                #     game_thread = threading.Thread(target = start_game_thread, args = (client,))
                #     game_thread.start()
                #     time.sleep(1)
                break
            else:
                broadcast(message)
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
            broadcast(str.encode(f'{game.get_top_card()}'))
            for client, name, player in player_list:
                while True:
                    client.send(str.encode("Press enter, then answer.\n"))
                    client.send(str.encode("Would you like to make top card trump? (Y/N)\n"))
                    message = client.recv(1024)
                    if message.decode("utf-8") == f"{name}: y" or message.decode("utf-8") == f"{name}: n":
                        break
                    else:
                        client.send(str.encode("Please input either a y or n."))  
                        continue
                    break
                if message.decode('utf-8').lower() == f"{name}: n":
                    client.send(str.encode("Received.\n"))
                    continue
                else:
                    pass
            print("finished")
            break
        except Exception as e:
            print(e)
            break

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

# def start_game_thread(client): # this is where the game is going to be played.
#     while True:
#         try:
#             # message = client.recv(1024)
#             # if message.decode("utf-8") != f"{names[0]}: ":
#             #     continue
            
#             # clients[0].send((str.encode("REPLY")))
#             message = client.recv(1024)
#             if message.decode("utf-8") == "a: reply":
#                 print("work!")
#                 clients[1].send((str.encode("REPLY")))
#                 if message.decode("utf-8") == "b: please?":
#                     print("nut")
#                 else:
#                     break
#             else:
#                 print(message.decode("utf-8"))
#                 print("didnt work")
#                 break
#             if not game.game_over:
#                 #broadcast(str.encode(f"The top card is, {game.get_top_card()}"))
#                 pass
#         except Exception as e:
#             print(e)
#             index = clients.index(client)
#             clients.remove(client)
#             name = names[index]
#             broadcast(f"{name} has left the game.".encode('utf-8'))
#             names.remove(name)
#             client.close()
#             print(str(len(clients))+ "/4 players are in")
#             break


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
