import socket
import threading
from queue import Queue

# Server configuration
HOST = 'localhost'
PORT = 2048
NUM_CLIENTS = 4

# Function to handle client connections
def handle_client(client_socket):
    # Perform operations with the client
    # Example: echo server
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        broadcast_data(data)
        client_socket.sendall(data)
    client_socket.close()

# Function to accept and handle client connections
def accept_connections(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_sockets.append(client_socket)

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def broadcast_data(data):
    for client_socket in client_sockets:
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
client_sockets = []

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
