import socket
from _thread import *
import sys
from game import *
# The local ip address the machine that is hosting the server is on
server = socket.gethostname()

# Safe port number to use.
port = 5555

# Type of socket. Sock stream is how the server string that comes into the server. 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binds the server and port to the socket.
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Number of client connections to the server. 4 because Euchre needs 4 players. Opens up the port.
s.listen(4)
print("Waiting for a connection...\nServer Started")

player_list_names = []

# Creates a threaded client when you connect. 
def threaded_client(conn, player):
    conn.send(str.encode("Your seat number is: " + str(original_seat_num)))
    reply = ""
    try:
        data = conn.recv(2048) # number of information we are receiving
        reply = data.decode("utf-8") # The encoding standard (utf-8)
        print("Received: ", reply)
        player_list_names.append(reply)
        print(player_list_names)
        conn.sendall(str.encode(reply)) # Encodes the string reply into bytes object
    except Exception as e:
        print(e)
        print("Lost connection") # If any erros occur, it will close the connection. 
        conn.close()

# Continuosly looks for connections and starts a threaded client.
original_seat_num = 0
while True:
    conn, addr = s.accept()
    original_seat_num += 1
    print("Connected to: " , addr)
    start_new_thread(threaded_client, (conn, original_seat_num))

