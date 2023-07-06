import socket
import sys

import random
from client import Client
from mao import Mao

baralho = [
    'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
]

# Classe que representa o servidor e suas operações
class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 2048
        self.size = 1024
        self.server = None
        self.threads = [] # Guarda as threads criadas para cada cliente conectado
        self.hand = Mao() # Cria a mão do Dealer (servidor)
        self.pause_counter = 2 # Usado para continuar a execução da thread principal - iniciar a vez do Dealer

    # Cria o socket e espera por, no máximo, 2 conexões
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(2)
        except socket.error (value,message):
            if self.server:
                self.server.close()
            print("Could not open socket: " + message)
            sys.exit(1)

    # Envia uma mensagem a todos os clientes conectados ao servidor
    def broadcast(self, msg):
        for client in self.threads:
            client_socket = client.client

            client_socket.send(msg.encode("utf-8"))
    
    # Envia uma mensagem requisitando uma entrada a um cliente específico
    def req_input(self, thread):
        thread.client.send("\nDeseja [M]ais uma carta ou quer [P]arar? ".encode("utf-8"))

    # Simula a vez de jogar do Dealer (servidor), jogando a mão dele e calculando os resultados finais do jogo
    def dealer_turn(self):
        self.broadcast(f"\nDealer mostra: [{self.hand.cartas[0]}, {self.hand.cartas[1]}]") # Dealer mostra sua segunda carta

        # Dealer recebe mais cartas até atingir pelo menos 17 pontos
        while self.hand.calcular_pontos() < 17:
            self.hand.receber_carta(random.choice(baralho))
            self.broadcast(str(self.hand.cartas))

        # Mostra as mãos e pontuações do jogador e do dealer
        for thread in self.threads:
            thread.client.send("\n--- Fim do jogo ---".encode("utf-8"))
            thread.client.send(f"\nSua mão: {thread.get_cartas()}".encode("utf-8"))
            thread.client.send(f"\nPontuação: {thread.calcular_pontos()}".encode("utf-8"))
        
        self.broadcast(f"\nMão do dealer: {self.hand.cartas}")
        self.broadcast(f"\nPontuação do dealer: {self.hand.calcular_pontos()}")

        pontos_dealer = self.hand.calcular_pontos()

        # Verifica o resultado do jogo
        for thread in self.threads:
            pontos_jogador = thread.calcular_pontos()

            if pontos_jogador > 21 and pontos_dealer <= 21:
                self.broadcast(f"\n{thread.name} perdeu para o Dealer!")
            elif (pontos_dealer <= 21 and pontos_jogador <= 21):
                if pontos_jogador > pontos_dealer:
                    self.broadcast(f"\n{thread.name} venceu o Dealer!")
                elif pontos_jogador < pontos_dealer:
                    self.broadcast(f"\n{thread.name} perdeu para o Dealer!")
                else:
                    self.broadcast(f"\n{thread.name} empatou com o Dealer!")
            elif pontos_dealer > 21 and pontos_jogador <= 21:
                self.broadcast(f"\n{thread.name} venceu o Dealer!")
            elif (pontos_dealer > 21 and pontos_jogador > 21):
                self.broadcast(f"\n{thread.name} e Dealer perderam!")

    # Função para iniciar um novo jogo - é executada por cada thread separadamente
    def blackjack(self, thread):
        print(thread)        

        # Inicializando a mão do jogador
        thread.hand = Mao()

        # Distribuindo duas cartas para o jogador
        for _ in range(2):
            thread.receber_carta(random.choice(baralho))

        # Loop do jogo
        while True:
            # Mostra as cartas do jogador e a primeira carta do dealer
            thread.client.send(f"\nSua mão: {thread.get_cartas()}".encode("utf-8"))
            thread.client.send(f"\nPontuação: {thread.calcular_pontos()}".encode("utf-8"))
            thread.client.send(f"\nDealer mostra: {self.hand.cartas[0]}".encode("utf-8"))

            # Verifica se o jogador já estourou 21 pontos
            if thread.calcular_pontos() > 21:
                thread.client.send("\nVocê estourou 21 pontos! Você perdeu.".encode("utf-8"))
                self.pause_counter -= 1
                break

            # Pergunta ao jogador se ele deseja receber mais uma carta ou parar
            self.req_input(thread)

            escolha = thread.client.recv(1024)
            if escolha.decode() == 'm':
                thread.receber_carta(random.choice(baralho))
            else:
                self.pause_counter -= 1
                break
    
    # Inicializa as operações do servidor
    def run(self):
        self.open_socket()

        # Distribuindo duas cartas para o Dealer
        for _ in range(2):
            self.hand.receber_carta(random.choice(baralho))

        running = 1
        while running: # Loop do servidor

            if len(self.threads) < 2: # Aceita conexões até que se tenham 2
                client, address = self.server.accept()
                c = Client(client, address, self.blackjack)
                c.start()
                self.threads.append(c)

            if self.pause_counter == 0: # Impede que o Dealer comece a sua vez antes que os jogadores terminem de jogar suas mãos
                running = 0

        self.dealer_turn()
        
        # Fecha todas as threads
        self.server.close()
        for c in self.threads:
            c.join()


if __name__ == "__main__":
    s = Server()
    s.run()