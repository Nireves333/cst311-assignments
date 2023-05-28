# Multithreading sockets are essential for handling multiple client connections
#  concurrently. Typically, a socket can only handle one connection at a time so
#  multiple threads are needed to handle concurrent client connections. When the
#  server accepts a client connection, it creates a dedicated thread to handle
#  that connection. Threads operate independently and concurrently, processing
#  incoming data and sending responses. This approach improves performance,
#  response time, and overall throughput of the server.

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

import socket as s
import logging
import threading

# Configure logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

# Array lists to store client ID's and their sockets
client_sockets = []
client_ids = []

def forward_message(sender_id, message):
    # Forward the message to the other client
    if sender_id == client_ids[0]:
        receiver_socket = client_sockets[1]
    else:
        receiver_socket = client_sockets[0]

    # Check if the receiver socket is still valid. This ensures that the 'bye' message is
    # sent and received bye the other client if the sending client socket has closed.
    if receiver_socket.fileno() != -1:
        receiver_socket.send(f"[{sender_id}]: {message}".encode())


def connection_handler(connection_socket, address, client_id):
    # Send the client's alias to the client
    connection_socket.send(client_id.encode())

    while True:
        # Read data from the new connection socket
        #  Note: if no data has been sent this blocks until there is data
        # Receive response, decode from UTF-8 bytestream
        query = connection_socket.recv(1024).decode()

        # Log the received message
        log.info("Received message from client " + client_id + ": " + query)

        # Check if the client wants to quit
        if query.lower() == 'bye':
            log.info("Client " + client_id + " disconnected.")

            # Forward "bye" message to the other client
            forward_message(client_id, query)
            break

        # Forward the message to the other client
        forward_message(client_id, query)

    # Close the client socket
    connection_socket.close()

def main():
    # Create a TCP socket
    # Notice the use of SOCK_STREAM for TCP packets
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Assign IP address and port number to socket, and bind to chosen port
    server_socket.bind(('', server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(2)

    # Alert user we are now online
    log.info("The server is ready to receive on port " + str(server_port))

    # Loop until the number of threads is received
    for thread_count in range(2):
        # When a client connects, create a new socket and record their address
        connection_socket, address = server_socket.accept()

        # Assign client ID
        if thread_count == 0:
            client_id = 'X'
        else:
            client_id = 'Y'

        # Server displays alias/client ID
        print("Connected to client at " + str(address) + " as " + client_id)

        # Add the client socket and ID to the respective lists
        client_sockets.append(connection_socket)
        client_ids.append(client_id)

        # Pass the new socket, address, and client ID to the connection handler function
        threading.Thread(target=connection_handler, args=(connection_socket, address, client_id)).start()

    server_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
    main()
