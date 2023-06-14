# Multithreading sockets are essential for handling multiple client connections
#  concurrently. Typically, a socket can only handle one connection at a time so
#  multiple threads are needed to handle concurrent client connections. When the
#  server accepts a client connection, it creates a dedicated thread to handle
#  that connection. Threads operate independently and concurrently, processing
#  incoming data and sending responses. This approach improves performance,
#  response time, and overall throughput of the server.

"""Chat server for CST311 Programming Assignment 3"""
"""Now converted to support SSL/TLS"""
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
import subprocess
import os
import ssl

# Configure logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

def connection_handler(connection_socket, address, client_id, messages):
  
  # Read data from the new connection socket
  #  Note: if no data has been sent this blocks until there is data
  # Receive response, decode from UTF-8 bytestream
  query = connection_socket.recv(1024).decode()
  
  # Log query information
  log.info("Recieved query test \"" + str(query) + "\"")
  
  # Store response to message list
  messages.append(client_id + ' : ' + query)
  # Loop until messages are received and stored
  while True:
    if(len(messages) == 2):
      break
  # Format response to client
  response = messages[0] + ', ' + messages[1]
  
  # Send response over the network, encoding to UTF-8
  response = messages[0] + ', ' + messages[1]
  connection_socket.send(response.encode())
  
  # Close client socket
  connection_socket.close()
  
        
def main():
  
  thread_count = 0
  messages = []
  
  #Generate CERTS/KEYS
  H4IP = "10.0.2.100"
  CN = input("Enter desired Common Name (CN) [format www.example.test]: ")
  subprocess.run(['python', "/home/mininet/CST311/Assignment4/cert.py", CN, H4IP])

  # Convert input to remove www. and .test for key/cert file names
  # Remove "www." prefix
  if CN.startswith("www."):
    CNbase = CN[4:]
        
  # Remove ".test" suffix
  if CNbase.endswith(".test"):
    CNbase = CNbase[:-5]
  
  # Variables, including location of server certificate and private key file
  server_address = "www." + CNbase + ".test"
  ssl_key_file = os.path.join("/home/mininet/CST311/private/", CNbase + "-key.pem")
  ssl_certificate_file = os.path.join("/home/mininet/CST311/newcerts/", CNbase + "-cert.pem")
  
  # Create an SSL/TLS context
  ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  # Load the server's certificate and private key
  ssl_context.load_cert_chain(ssl_certificate_file, ssl_key_file)

  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Wrap the server socket with the SSL/TLS context
  server_socket = ssl_context.wrap_socket(server_socket, server_side=True)
  
  # Assign IP address and port number to socket, and bind to chosen port
  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(2)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))
  
  # Loop until number of threads is received
  for thread_count in range(2):
      
    # When a client connects, create a new socket and record their address
    connection_socket, address = server_socket.accept()
    log.info("Connected to client at " + str(address))
      
    # Assign client ID
    if thread_count == 0:
      client_id = 'X'
    else:
      client_id = 'Y'
      
    # Pass the new socket and address off to a connection handler function
    threading.Thread(target=connection_handler, args=(connection_socket, address, client_id, messages)).start()
      
    # Increment thread count
    thread_count += 1
      
  server_socket.close()

if __name__ == "__main__":
  main()
