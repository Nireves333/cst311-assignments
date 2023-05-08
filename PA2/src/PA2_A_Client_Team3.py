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
    
    # List to store sample_rtt, estimated_rtt, and dev_rtt values
    sample_rtt = []
    estimated_rtt = []
    dev_rtt = []
    
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
          sample_rtt.append(elapsed)
          
          # Set initial ERTT or calculate current ERTT, formula taken from textbook
          #or (i < len(estimated_rtt) and estimated_rtt[i] == 0):
          if len(estimated_rtt) == 0: 
            est_elapsed = elapsed
            estimated_rtt.append(elapsed)
          else:
            est_elapsed = (0.875 * est_elapsed) + (0.125 * elapsed)
            estimated_rtt.append(est_elapsed)
          
          # Set initial Dev_RTT or calculate current Dev_RTT, formula taken from textbook
          #or (i < len(dev_rtt) and dev_rtt[i] == 0):
          if len(dev_rtt) == 0: 
            dev_elapsed = elapsed / 2
            dev_rtt.append(dev_elapsed)
          else:
            dev_elapsed = (0.75 * dev_elapsed) + (.25 * abs(elapsed - est_elapsed))
            dev_rtt.append(dev_elapsed)
               
          # Print message
          print('Ping {}: sample_rtt = {:.3f} ms, estimated_rtt = {:.3f} ms, dev_rtt = {:.3f} ms'.format(i, elapsed, est_elapsed, dev_elapsed))
      
      # Exception happens when timeout is one second or more
      except s.timeout:
          # Print message
          sample_rtt.append(0)
          estimated_rtt.append(0)
          dev_rtt.append(0)
          print('Ping {}: Request timed out'.format(str(i)))
    
    #DEBUG
    for i, num in enumerate(estimated_rtt):
      print("estimated_rrt:", num)
    
    # Print summary values header
    print('Summary values:')
    # Print minimum RTT value
    print('min_rtt = {:.3f} ms'.format(min(sample_rtt)))
    # Print maximum RTT value
    print('max_rtt = {:.3f} ms'.format(max(sample_rtt)))
    # Calculate and print mean RTT value
    mean = sum(sample_rtt) / float(len(sample_rtt))
    print('ave_rtt = {:.3f} ms'.format(mean))
    # Print packet loss percentage
    print('Packet loss: {:.2f}%'.format((10 - len(sample_rtt)) * 10))
    
    ## TODO calculate timeout interval, broken at the moment
    # Books formula: TimeoutInterval = EstimatedRTT + 4 x DevRTT
    final_est = 0
    final_dev = 0
    for est, dev in zip(estimated_rtt, dev_rtt):
      print('final est: {:.3f} ms'.format(final_est))
      print('final_dev: {:.3f} ms'.format(final_dev))
      final_est = final_est + est
      final_dev = final_dev + dev
    TimeoutInterval = final_est + (4 * final_dev)
    print('Timeout Interval: {:.3f} ms\n'.format(TimeoutInterval))  
    
  # Close socket    
  socket.close()
    
if __name__ == "__main__":
  main()