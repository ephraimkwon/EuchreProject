import socket
from _thread import *
import sys

# The local ip address the machine that is hosting the server is on
server = "128.61.83.84"

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

# Creates a threaded client when you connect. 
def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048) # number of information we are receiving
            reply = data.decode("utf-8") # The encoding standard (utf-8)
            if not data:
                print("Disconnected") # If the data is not being received from the client, it will disconnect
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply)) # Encodes the string reply into bytes object
        except:
            break

    print("Lost connection") # If any erros occur, it will close the connection. 
    conn.close()

# Continuosly looks for connections and starts a threaded client.
while True:
    conn, addr = s.accept()
    print("Connected to: " , addr)
    start_new_thread(threaded_client, (conn,))
