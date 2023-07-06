import threading
import socket

class Client(threading.Thread):
    def __init__(self, client, address, target_func):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.hand = None
        self.target_func = target_func

    def get_cartas(self):
        return self.hand.cartas

    def receber_carta(self, carta):
        self.hand.receber_carta(carta)
    
    def calcular_pontos(self):
        return self.hand.calcular_pontos()

    def run(self):
        self.client.send(f"Você --> {self.name}".encode("utf-8"))
        print(threading.main_thread())
        self.target_func(self)

        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                self.client.send(data)
                print(data.decode('utf-8'))
            else:
                self.client.close()
                running = 0