import socket
import threading

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




def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "eph: test":
                clients[0].send(str.encode("Fuck"))
            else:
                broadcast(message)
        except Exception as e:
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
        thread = threading.Thread(target = handle, args = (conn,))
        thread.start()


print("Server started. Waiting for connections...")

receive()
