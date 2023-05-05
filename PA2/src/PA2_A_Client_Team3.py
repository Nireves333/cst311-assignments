"""UDP client for CST311 Programming Assignment 2"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

# Import the socket module as a named module to help keep our namespace clean
import socket as s
import os
import subprocess
import time

# Import and configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# DELETE? import PA2_A_Server_Team3

server_host = '10.0.0.1'
server_port = 12001

def main():
  
  # Create the socket
  with s.socket(s.AF_INET, s.SOCK_DGRAM) as socket:
    
    # Set timeout at 1 second
    socket.settimeout(1)
    
    # List to store RTT values
    rtt = []
    
    # Ping server 10 times
    for i in range(1, 11):
      
      try:
        ## TODO check if ping should actually be used or client sends message because server code has a message received line in code
        # Execute ping command and get output
        ping_output = subprocess.check_output(['ping', '-c', '1', server_host]).decode()
        
        # Extract RTT value from ping output
        for line in ping_output.split('\n'):
          if 'time=' in line:
            rtt_str = line.split('time=')[1].split(' ')[0]
            # Store RTT value
            rtt.append(float(rtt_str))
        
        ## TODO fix print message to match expected output (need sample_rtt, estimated_rtt, dev_rtt)
        # Print message
        print('Ping {}: rtt = {} ms'.format(str(i), rtt_str))
      
      ## TODO fix timeout because it is not working properly
      except s.timeout:
        # Print message
        print('Ping {}: Request timed out'.format(str(i)))
    
    # Print summary values
    print('Summary values')
    print('min_rtt = {} ms'.format(min(rtt)))
    print('max_rtt = {} ms'.format(max(rtt)))
    mean = sum(rtt) / float(len(rtt))
    print('ave_rtt = {} ms'.format(mean))
    print('Packet loss: {}%'.format((10 - len(rtt)) * 10))
    ## TODO calculate timeout interval
    print('Timeout Interval: ms')
      
  # Close socket    
  socket.close()
    
if __name__ == "__main__":
  main()
