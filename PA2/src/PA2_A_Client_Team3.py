"""UDP client for CST311 Programming Assignment 2"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

import socket as s
import time
import PA2_A_Server_Team3

server_host = '10.0.0.1'
server_port = PA2_A_Server_Team3.SERVER_PORT

def main():
  
  # Create the socket
  with s.socket(s.AF_INET, s.SOCK_DGRAM) as socket:
    
    # Set timeout at 1 second
    socket.settimeout(1)
    
    # List to store RTT values
    rtt = []
    
    # Ping server 10 times
    for i in range(1, 11):
      
      # Get start time
      start_time = time.time()
      message = 'Ping {}'.format(str(i))
      
      # Try to send message
      try:
        
        # Send message to server
        socket.sendto(message.encode(), (server_host, server_port))
        
        # If no message received from server
        if socket.recvfrom(1024) == None:
          print('Ping {}: Request timed out'.format(str(i)))
        
        # Otherwise, record RTT values
        else:
          
          # Get end time
          end_time = time.time()
        
          # Calculate elapsed time aka RTT
          elapsed = (end_time - start_time) * 1000
        
          # Add RTT value to list
          rtt.append(elapsed)
        
          ## TODO fix print message to match expected output (need sample_rtt, estimated_rtt, dev_rtt)
          # Print message
          print('Ping {}: rtt = {:.3f} ms'.format(str(i), elapsed))
      
      # Exception happens when timeout is one second or more
      except s.timeout:
          # Print message
          print('Ping {}: Request timed out'.format(str(i)))
    
    # Print summary values header
    print('Summary values:')
    # Print minimum RTT value
    print('min_rtt = {:.3f} ms'.format(min(rtt)))
    # Print maximum RTT value
    print('max_rtt = {:.3f} ms'.format(max(rtt)))
    # Calculate and print mean RTT value
    mean = sum(rtt) / float(len(rtt))
    print('ave_rtt = {:.3f} ms'.format(mean))
    # Print packet loss percentage
    print('Packet loss: {:.2f}%'.format((10 - len(rtt)) * 10))
    ## TODO calculate timeout interval
    print('Timeout Interval: ms\n')
      
  # Close socket    
  socket.close()
    
if __name__ == "__main__":
  main()
