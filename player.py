from mao import Mao

class Player:
    def __init__(self, client_socket, addr):
        self.hand = Mao()
        self.client_socket = client_socket
        self.addr = addr
    
    def getClientSocket(self):
        return self.client_socket
    
    def getClientAddr(self):
        return self.addr

    def getClientHand(self):
        return self.hand
    
    def receber_carta(self, carta):
        self.hand.receber_carta(carta)
    
    def calcular_pontos(self):
        return self.hand.calcular_pontos()