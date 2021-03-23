import socket
import threading
from game_online import *

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
            if len(clients) == 4:
                broadcast(str.encode("Let's begin!\n Setting up players..."))
                game.set_up(names)
                for client in clients:
                    game_thread = threading.Thread(target = start_game, args = (client,))
                    game_thread.start()
                break
                
            elif message.decode('utf-8') == "a: test":
                print("Interesting")
                for client in clients:
                    game_thread = threading.Thread(target = start_game, args = (client,))
                    game_thread.start()
                game.set_up(names)
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

def start_game(client):
    while True:
        try:
            message = client.recv(1024)
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
