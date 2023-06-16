"""TLS webserver certificate for CST311 Programming Assignment 4"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

import subprocess
import os
import sys

# Check if folders for certificates exist, otherwise create them
if not os.path.exists("/home/mininet/CST311/certs"):
  os.mkdir('/home/mininet/CST311/certs')
if not os.path.exists("/home/mininet/CST311/newcerts"):
  os.mkdir('/home/mininet/CST311/newcerts')
if not os.path.exists("/home/mininet/CST311/private"):
  os.mkdir('/home/mininet/CST311/private')

# Working directory
working_dir = '/home/mininet/CST311/certs'

# Generate CA private key
subprocess.call(['sudo', 'openssl', 'genrsa', '-aes256', '-out', 'cakey.pem', '-passout', 'pass:1234', '2048'], cwd=working_dir)

# Create root CA signing certificate
subprocess.call(['sudo', 'openssl', 'req', '-x509', '-new', '-nodes', '-key', 'cakey.pem', '-sha256', '-days', '1825', '-out', 'cacert.pem', '-passin', 'pass:1234', '-subj', '/C=US/ST=CA/L=Monterey/O=CST311/OU=Networking/CN=ca.pa4.test'], cwd=working_dir)

# Move root key into private directory
subprocess.call(['sudo', 'mv', './cakey.pem', './private'], cwd=working_dir)

# Copy root CA into directory
subprocess.call(['sudo', 'cp', 'cacert.pem', '/usr/local/share/ca-certificates/cacert.crt'], cwd=working_dir)

# Run ca-certificates application
subprocess.call(['sudo', 'update-ca-certificates'])

# Retrieve the passed variables
CN = sys.argv[1]
hostIP = sys.argv[2]

# Convert input to remove www. and .test for key/cert file names
# Remove "www." prefix
if CN.startswith("www."):
  CNbase = CN[4:]
        
# Remove ".test" suffix
if CNbase.endswith(".test"):
  CNbase = CNbase[:-5]

# Generate private key for server
subprocess.call(['sudo', 'openssl', 'genrsa', '-out', CNbase + '-key.pem', '-passout', 'pass:1234', '2048'], cwd=working_dir)

# Generate certificate signing request using server private key
subprocess.call(['sudo', 'openssl', 'req', '-nodes', '-new', '-config', '/etc/ssl/openssl.cnf', '-key', CNbase + '-key.pem', '-out', CNbase + '.csr', '-subj', '/C=US/ST=CA/L=Monterey/O=CST311/OU=Networking/CN=' + CN], cwd=working_dir)

# Create server certificate
subprocess.call(['sudo', 'openssl', 'x509', '-req', '-days', '365', '-in', CNbase + '.csr', '-CA', 'cacert.pem', '-CAkey', './private', '-CAcreateserial', '-out', CNbase + '-cert.pem', '-passin', 'pass:1234'], cwd=working_dir)

# Copy certificate and key into subdirectories
subprocess.call(['sudo', 'mv', './' + CNbase + '-cert.pem', "/home/mininet/CST311/newcerts/"], cwd=working_dir)
subprocess.call(['sudo', 'mv', './' + CNbase + '-key.pem', "/home/mininet/CST311/private/"], cwd=working_dir)

# Protect server’s private key
subprocess.call(['sudo', 'chmod', '-R', '600', 'private'], cwd=working_dir) 

# Modify host file to include IP addresses
subprocess.call(['sudo', 'sh', '-c', 'echo "127.0.0.1\tca.pa4.test" >> /etc/hosts'])
subprocess.call(['sudo', 'sh', '-c', 'echo "' + hostIP + '\t' + CN + '" >> /etc/hosts'])

# Move cacert.pem to ssl/certs folder
file_path = '/home/mininet/CST311/cacert.pem'

if os.path.exists(file_path):
  subprocess.call (['sudo', 'mv' , "/home/mininet/CST311/cacert.pem" , "/etc/ssl/certs/"])

# Run ca-certificates application
subprocess.call(['sudo', 'update-ca-certificates'])

# Print success message
print('***Server Certificate Issued***')
