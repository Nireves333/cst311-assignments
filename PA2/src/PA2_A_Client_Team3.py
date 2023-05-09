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
    
    # Lists to store RTT values
    sample_rtt = []
    estimated_rtt = []
    dev_rtt = []
    
    # Set timeout at 1 second
    socket.settimeout(1)
    # Initialize elapsed time
    elapsed = 0
    
    # Ping server 10 times
    for i in range(1, 11):
      
      # Get start time
      start_time = time.time()
      # Initialize message
      message = 'Ping {}'.format(str(i))
      # Send message to server
      socket.sendto(message.encode(), (server_host, server_port))
      
      # Try to receive reply
      try:
        reply, _ = socket.recvfrom(1024)
        # Get end time
        end_time = time.time()
        # Calculate elapsed time aka sample RTT
        elapsed = (end_time - start_time) * 1000
        # Add sample RTT to list
        sample_rtt.append(elapsed)
          
        # Set initial estimated RTT or calculate current estimated RTT and add to list
        # Formula from textbook, page ???
        if len(estimated_rtt) == 0:
          est_elapsed = elapsed
          estimated_rtt.append(est_elapsed)
        else:
          est_elapsed = (0.875 * est_elapsed) + (0.125 * elapsed)
          estimated_rtt.append(est_elapsed)
          
        # Set initial dev RTT or calculate current dev RTT and add to list
        # Formula from textbook, page ???
        if len(dev_rtt) == 0:
          dev_elapsed = elapsed / 2
          dev_rtt.append(dev_elapsed)
        else:
          dev_elapsed = (0.75 * dev_elapsed) + (0.25 * abs(elapsed - est_elapsed))
          dev_rtt.append(dev_elapsed)
               
        # Print results
        print('Ping {}: sample_rtt = {:.3f} ms, estimated_rtt = {:.3f} ms, dev_rtt = {:.3f} ms'.format(i, elapsed, est_elapsed, dev_elapsed))
        
      # Throw exception when timeout occurs
      except s.timeout:
        # Print message
        print('Ping {}: Request timed out'.format(str(i)))
        # Add RTT values to list
        sample_rtt.append(0)
        estimated_rtt.append(0)
        dev_rtt.append(0)
    
    # Print header
    print('Summary values:')
    
    # Print minimum RTT value
    print('min_rtt = {:.3f} ms'.format(min(sample_rtt)))
    
    # Print maximum RTT value
    print('max_rtt = {:.3f} ms'.format(max(sample_rtt)))
    
    # Calculate and print mean RTT value
    mean = sum(sample_rtt) / float((len(sample_rtt) - sample_rtt.count(0)))
    print('ave_rtt = {:.3f} ms'.format(mean))
    
    # Print packet loss percentage
    loss = sample_rtt.count(0) / len(sample_rtt) * 100
    print('Packet loss: {:.2f}%'.format(loss))
    
    # Calculate timeout interval by using the last index of estimated_rtt and dev_rtt
    # Initialize final_est and final_dev
    final_est = 0
    final_dev = 0
    # Get last float that is not 0 in estimated_rtt list
    for i, est in enumerate(reversed(estimated_rtt)):
      if est > 0:
        final_est = est
        break
    # Get last float that is not 0 in dev_rtt list
    for i, dev in enumerate(reversed(dev_rtt)):
      if est > 0:
        final_dev = dev
        break
    # Calculate timeout interval
    # Formula from textbook, page ???
    timeout_interval = final_est + (4 * final_dev)
    # Print timeout interval
    print('Timeout interval: {:.3f} ms\n'.format(timeout_interval))  
    
  # Close socket    
  socket.close()
    
if __name__ == "__main__":
  main()
  
