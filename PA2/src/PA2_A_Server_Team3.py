"""UDP server for CST311 Programming Assignment 2"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

import random
import socket as s

SERVER_PORT = 12000

def main():
  
  # Create a UDP socket
  # Notice the use of SOCK_DGRAM for UDP packets
  with s.socket(s.AF_INET, s.SOCK_DGRAM) as socket:
  
    # Assign IP address and port number to socket
    socket.bind(('', SERVER_PORT))
    
    # Print statement
    print("Waiting for client...")
    
    # Initialize ping count
    pingnum = 0
  
    while True:
    
      # Count the pings received
      pingnum += 1
    
      # Generate random number in the range of 0 to 10
      rand = random.randint(0, 10)
    
      # Receive the client packet along with the
      # address it is coming from
      message, address = socket.recvfrom(1024)
    
      # If rand is less is than 4, and this not the
      # first "ping" of a group of 10, consider the
      # packet lost and do not respond
      if rand < 4 and pingnum % 10 != 1:
        print('\nPacket was lost')
        continue
      
      # Otherwise, the server responds
      else:
        # Print the current ping count
        print('\nPING {}'.format(pingnum))
        # Print message received from client
        print('Mesg rcvd: {}'.format(message.decode()))
        # Decode the message and convert the message to uppercase
        response_msg = message.decode().upper()
        # Print decoded, converted message
        print('Mesg sent: {}'.format(response_msg))
        # Encode the message string back to a UTF-8 bytestream
        response = response_msg.encode()
        # Send the encoded message back to the client
        socket.sendto(response, address)
        continue

if __name__ == "__main__":
  main()
