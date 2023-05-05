#!env python
"""UDP server for CST311 Programming Assignment 2"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

# Imports so far
import logging
import os
import socket as s

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import PA2_A_Server_Team3

server_host = '10.0.0.1'
server_port = PA2_A_Server_Team3.SERVER_PORT

# Simple ping test, needs to be modified. 
ping = os.system("ping -c 10 " + server_host)
log.info(ping)