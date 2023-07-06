import threading

# Classe que representa os clientes - cada cliente conectado é uma thread diferente dentro do servidor
class Client(threading.Thread): # Herda de Thread
    def __init__(self, client, address, target_func):
        threading.Thread.__init__(self)
        self.client = client # Socket proveniente da conexão do cliente
        self.address = address # Endereço proveniente da conexão do cliente
        self.size = 1024
        self.hand = None
        self.target_func = target_func # Função a ser executada pela thread

    def get_cartas(self):
        return self.hand.cartas

    def receber_carta(self, carta): # Delega a responsabilidade à classe Mao()
        self.hand.receber_carta(carta)
    
    def calcular_pontos(self): # Delega a responsabilidade à classe Mao()
        return self.hand.calcular_pontos()

    # Inicializa as operações do cliente
    def run(self):
        self.client.send(f"Você --> {self.name}".encode("utf-8")) # Exibe o nome do jogador
        print(threading.main_thread())
        self.target_func(self) # Executa a target_func passada como argumento no construtor

        running = 1
        while running: # Loop do cliente
            data = self.client.recv(self.size)
            if data:
                self.client.send(data)
                print(data.decode('utf-8'))
            else:
                self.client.close()
                running = 0