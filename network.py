import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostname()
        self.port = 5555 
        self.addr = (self.server, self.port)
        self.seat = self.connect()
        print(self.seat)

    def get_seat(self):
        return self.seat

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() 
        except:
            pass
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
    
    def listen(self):
        message = self.client.recv(2048).decode()
        return message
        
