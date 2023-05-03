import socket
import threading
import time

class Tracker:
    def __init__(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(('8.8.8.8', 1))
            local_ip_address = sock.getsockname()[0]
            sock.close()
        except:
            return None
        self.host = local_ip_address
        self.port = 5050
        self.addr = (self.host, self.port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        self.server.listen()
        self.clients = []
    
    def broadcast(self, msg):
        for sock in self.clients:
            sock.send(msg)
    def register(self, sock):
        self.clients.append(sock)
    def unregister(self, sock):
        self.clients.remove(sock)
    def printdata(self,msg):
        print(msg.decode("utf-8"))
    def handle(self, sock, addr):
        while True:
            try:
                data = sock.recv(1024)
                self.broadcast(data)
                self.printdata(data)
                
            except:
                self.unregister(sock)
                sock.close()
                break
    def run(self):
        while True:
            sock, addr = self.server.accept()
            self.register(sock)
            thread = threading.Thread(target=self.handle, args=(sock, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    tracker = Tracker()
    print("[STARTING] Server is starting...")
    tracker.run()
    