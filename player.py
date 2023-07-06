import socket
from threading import Thread

# Server configuration
HOST = 'localhost'
PORT = 2048

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print("\n==================================BlackJack==================================")

    while True:
        # Receive the server's response
        data = client_socket.recv(1024)
        if data.decode().endswith("input"):
            res = input("\nDeseja [M]ais uma carta ou quer [P]arar? ").lower()
            client_socket.send(res.encode("utf-8"))
        else:
            print(data.decode())

except KeyboardInterrupt:
    print("Client disconnect.")
finally:
    # Close the client socket
    client_socket.close()