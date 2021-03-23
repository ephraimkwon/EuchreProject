import socket
import threading

host = socket.gethostbyname(socket.gethostname())

port = 5555

name = input("Input your name: \n")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NAME":
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(e)
            client.close()
            break

def write():
    message = f"{name}: {input()}"
    client.send(message.encode('utf-8'))


recieve_thread = threading.Thread(target = receive)

write_thread = threading.Thread(target = write)

recieve_thread.start()
write_thread.start()