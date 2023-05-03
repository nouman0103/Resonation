import socket
from random import randint
import time

class Client:
    def __init__(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(('8.8.8.8', 1))
            local_ip_address = sock.getsockname()[0]
            sock.close()
        except:
            return None
        self.host = local_ip_address
        self.port = randint(5100, 6000)
        self.addr = (self.host, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def register(self):
        # Scan the Network and find the tracker on host and port 5050
        ip = self.host.rsplit('.',1)[0]
        self.client.settimeout(3)
        for (i) in range(1, 255):
            print(ip + '.' + str(i))
            try:
                self.client.connect((ip+'.'+str(i), 5050))
                self.client.send(self.addr.encode())
                return True
            except:
                continue

    def printclient(self):
        print(self.host, self.port)
    


if __name__ == "__main__":
    # Connect to server at ip 192.168.0.162 port 5050
    client = Client()
    client.register()
    client.printclient()