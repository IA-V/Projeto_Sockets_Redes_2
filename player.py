import socket

# Configuração do servidor do jogo
HOST = 'localhost'
PORT = 2048

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Cliente conecta-se ao servidor
    client_socket.connect((HOST, PORT))
    print("\n==================================BlackJack==================================")

    while True: # Loop para recebimento e tratamento das mensagens do servidor
        
        data = client_socket.recv(1024)
        if data.decode().endswith("input"): # Se o servidor requisitou entrada, exibe a mensagem de entrada
            res = input("\nDeseja [M]ais uma carta ou quer [P]arar? ").lower()
            client_socket.send(res.encode("utf-8"))
        else:
            print(data.decode())

except KeyboardInterrupt:
    print("Cliente desconectou.")
finally:
    # Fecha o socket
    client_socket.close()