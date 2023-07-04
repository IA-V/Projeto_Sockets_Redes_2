from socket import *
import threading

# Function to receive broadcast messages from the server
def receive_messages(client_socket):
    while True:
        #try:
            data = client_socket.recv(1024)
            msg_type = data.decode()[1]
            msg = data.decode()[0]

            if not data:
                break
            elif msg_type == 1:
                res = input(msg).lower()
                client_socket.send([res, 1])
            else:
                print("Dealer: ", data.decode())
            """except socket.error as error:
            # Handle socket errors if any
            print("Error receiving data from the server.")
            break"""

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
        message += '_0'
        client_socket.sendall(message.encode())
except KeyboardInterrupt:
    # Stop the client on keyboard interrupt
    print("Client stopped.")

client_socket.close()