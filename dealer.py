import random

import socket
import threading
from queue import Queue
from mao import Mao
from player import Player


# --------------------------------------------------------------------------------JOGO--------------------------------------------------------------------------------

# Definindo as cartas e seus valores
baralho = [
    'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
]

def player_input_action(player, escolha):
    p_addr = player.getClientAddr()
    p_hand = player.getClientHand()

    if escolha == 'm':
        player.receber_carta(random.choice(baralho))
    else:
        # Jogador parou, agora é a vez do dealer
        # Dealer recebe mais cartas até atingir pelo menos 17 pontos
        while HAND.calcular_pontos() < 17:
            HAND.receber_carta(random.choice(baralho))

        # Mostra as mãos do jogador e do dealer
        send_client_data("\n--- Fim do jogo ---", p_addr)
        send_client_data(f"Sua mão:  {p_hand.cartas}", p_addr)
        send_client_data(f"Pontuação: {player.calcular_pontos()}", p_addr)
        send_client_data(f"Mão do dealer: {HAND.cartas}", p_addr)
        send_client_data(f"Pontuação do dealer: {HAND.calcular_pontos()}", p_addr)

        # Verifica o resultado do jogo
        pontos_jogador = player.calcular_pontos()
        pontos_dealer = HAND.calcular_pontos()

        if pontos_jogador > pontos_dealer:
            send_client_data("Você venceu!", p_addr)
        elif pontos_jogador < pontos_dealer:
            send_client_data("Você perdeu!", p_addr)
        else:
            send_client_data("Empate!", p_addr)

        quit()


def novo_jogo():
    # Inicializando as mãos dos jogadores e do dealer
    HAND = Mao()
    HAND.receber_carta(random.choice(baralho)) # carta 1 do Dealer
    HAND.receber_carta(random.choice(baralho)) # carta 2 do Dealer

    # Distribuindo duas cartas para cada jogador
    for player in players:
        for _ in range(2):
            player.receber_carta(random.choice(baralho))

    # Loop do jogo
    while True:
        # Mostra as cartas do jogador e a primeira carta do dealer
        for player in players:
            p_addr = player.getClientAddr()
            p_hand = player.getClientHand()

            msg = f"\nSua mão: {p_hand.cartas}\nPontuação: {p_hand.calcular_pontos()}\nDealer mostra: {HAND.cartas[0]}"
            send_client_data(msg, p_addr)


            # Verifica se o jogador já estourou 21 pontos
            if player.calcular_pontos() > 21:
                send_client_data("Você estourou 21 pontos! Você perdeu.", p_addr)
                break

            # Pergunta ao jogador se ele deseja receber mais uma carta ou parar
            send_client_data("Deseja [M]ais uma carta ou quer [P]arar? ", p_addr, 1) # Como solicitar entrada ao player?
            # escolha = input("Deseja [M]ais uma carta ou quer [P]arar? ").lower()
            # player_input_action(player, escolha)

# --------------------------------------------------------------------------------SERVIDOR--------------------------------------------------------------------------------

HOST = 'localhost'
PORT = 2048
NUM_CLIENTS = 4
HAND = None

def send_client_data(data, addr, msg_type=0): # 0 -> mensagem comum; 1 -> mensagem de input()
    data = [data, msg_type]
    for player in players:
        p_addr = player.getClientAddr()
        client_socket = player.getClientSocket()
        if addr == p_addr:
            client_socket.sendall(data)

# Function to handle client connections
def handle_client(player):
    client_socket = player.getClientSocket()
    # Perform operations with the client
    # Example: echo server
    while True:
        data = client_socket.recv(1024)
        msg_type = data[1]
        msg = data[0]

        if not data:
            break
        elif msg_type == 1: # 0 -> mensagem comum; 1 -> mensagem de resposta a um input()
            player_input_action(player, msg)
        else:
            broadcast_client_data(data)
            client_socket.sendall(data)
    client_socket.close()

# Function to accept and handle client connections
def accept_connections(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        player = Player(client_socket, addr)
        players.append(player)

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(player,))
        client_thread.start()

        if len(players) >= 2:
            novo_jogo()

def broadcast_client_data(data):
    for player in players:
        client_socket = player.getClientSocket()
        try:
            client_socket.sendall(data)
        except socket.error:
            # Handle socket errors if any
            print("Error broadcasting data to a client.")

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(NUM_CLIENTS)
print(f"Server listening on {HOST}:{PORT}")

# Create a queue to hold the client threads
client_threads = []

# Lista de clientes conectados
players = []

# Start accepting connections in a separate thread
accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
accept_thread.start()

# Add the accept thread to the client threads queue
client_threads.append(accept_thread)

try:
    # Wait for all client threads to finish
    for thread in client_threads:
        thread.join()
except KeyboardInterrupt:
    # Stop the server on keyboard interrupt
    print("Server stopped.")
finally:
    # Close the server socket
    server_socket.close()