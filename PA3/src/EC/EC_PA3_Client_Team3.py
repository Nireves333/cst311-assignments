"""Chat client for CST311 Programming Assignment 3 Extra Credit"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

# Import statements
import socket as s
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = 'localhost'
server_port = 12000

def receive_messages(client_socket, client_id):
    while True:
        try:
            # Read response from server
            server_response = client_socket.recv(1024)
            # Decode server response from UTF-8 bytestream
            server_response_decoded = server_response.decode()

            # Splits the received message in two parts, the sender ID and
            # the message. We do this in order to differentiate the message 
            # portion from the client ID. Specifically to determine if the 
            # message contains 'bye'
            split_response = server_response_decoded.split(': ',1)
            sender_id = split_response[0]
            message = split_response[1]

            # Print the received message along with the sender's client ID
            if sender_id != client_id:
                print(f"{sender_id}: {message}")

                # Check if the message is "Bye" to exit
                # Sends a message notifying that client has disconnected
                if message.lower() == 'bye':
                    print("Partner has disconnected, type 'bye' to exit")
                    break
                    
        except IndexError:
          pass
        except ConnectionAbortedError:
          break
        except OSError as e:
          break

def main():
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    try:
        # Establish TCP connection
        client_socket.connect((server_name, server_port))

        # Receive the client's alias/ID from the server
        client_id = client_socket.recv(1024).decode()

    except Exception as e:
        log.exception(e)
        log.error("***Advice:***")
        if isinstance(e, s.gaierror):
            log.error("\tCheck that server_name and server_port are set correctly.")
        elif isinstance(e, ConnectionRefusedError):
            log.error("\tCheck that server is running and the address is correct")
        else:
            log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
        exit(8)

    try:
        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_id))
        receive_thread.start()
        print(f"You are connected as {client_id} (type 'bye' to exit)")

        while True:
            # Get input from user
            user_input = input()

            # Send message to the server
            client_socket.send(user_input.encode())

            # Check if the user wants to quit
            if user_input.lower() == "bye":
                break

    finally:
        # Close socket prior to exit
        client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
    main()
