from socket import *
import threading

# Function to receive broadcast messages from the server
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received:", data.decode())
        except socket.error:
            # Handle socket errors if any
            print("Error receiving data from the server.")
            break

serverName = 'localhost'
serverPort = 2048

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((serverName,serverPort))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

try:
    # Main client loop
    while True:
        # Get user input to send to the server
        message = input("Enter a message to send to the server (or 'exit' to quit): ")
        if message == 'exit':
            break
        # Send the message to the server
        client_socket.sendall(message.encode())
except KeyboardInterrupt:
    # Stop the client on keyboard interrupt
    print("Client stopped.")

client_socket.close()