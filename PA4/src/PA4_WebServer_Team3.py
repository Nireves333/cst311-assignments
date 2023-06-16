"""TLS webserver for CST311 Programming Assignment 4"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

import http.server
import ssl
import subprocess
import os

# Set variables used by cert.py before running
H2IP = "10.0.1.100"
CN = "www.webtest.test"
print("Common Name is", CN)

# Generate CERTS/KEYS
subprocess.run(['python', "/home/mininet/CST311/Assignment4/PA4_Cert_Team3.py", CN, H2IP])

# Convert input to remove www. and .com for key/cert file names
# Remove "www." prefix
if CN.startswith("www."):
  CNbase = CN[4:]
        
# Remove ".test" suffix
if CNbase.endswith(".test"):
  CNbase = CNbase[:-5]
  
# Variables, including location of server certificate and private key file
server_address = "www." + CNbase + ".test"
server_port = 4443
ssl_key_file = os.path.join("/home/mininet/CST311/private/", CNbase + "-key.pem")
ssl_certificate_file = os.path.join("/home/mininet/CST311/newcerts/", CNbase + "-cert.pem")

#Context is the TLS Server with its certificate file and key file location
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(ssl_certificate_file, ssl_key_file)
 
## Don't modify anything below
httpd = http.server.HTTPServer((server_address, server_port), http.server.SimpleHTTPRequestHandler)
httpd.socket = context.wrap_socket(httpd.socket,
               server_side=True)

print("Listening on port", server_port)                                
httpd.serve_forever()
