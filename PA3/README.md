# Programming Assignment 3
## CST 311, Introduction to Computer Networks

READ INSTRUCTIONS CAREFULLY BEFORE YOU START THE ASSIGNMENT.

Assignment must be submitted electronically to iLearn on https://csumb.instructure.com/ by 11:59 p.m. on the due date.  Late assignments will not be accepted. 
Use the Teams on the Programming Assignment Teams document (also on Canvas under General Information -> Team Information)
Select your Team leader and divide up work per the Programming Process instructions (also on Canvas under General Information > Team Information.)

The assignment requires you to submit both client and server programs. The naming convention of the file should be PA3_Server_Team<your team #>.py and PA3_Client_Team<your team #>.py
Put your names in the program as well. Your client and server programs must meet the requirements below. Your program must have sufficient comments to clearly explain how your code works. Your code must compile to get partial credit.

This assignment is worth 150 points. 

## Purpose

The purpose of this assignment is to satisfy one of the stated outcomes in the syllabus:
- Develop simple software programs using sockets to achieve communication between two (or more) computers.

You will write the program in Python where the interface to the TCP/IP application programming interface is similar to other C-family programming languages.

## Context
The Transmission Control Protocol allows for connection-oriented sessions between clients and a server. This means that multiple clients can connect to a single server and the communication is managed in separate sessions for each client. The initial connection setup is done once and then packets are exchanged until the connection is closed. A common pattern is for a TCP server to start up and allow multiple connections; in fact, this is exactly how HTTP web servers work.
There are an endless number of applications that rely on the kind of communication service that you will develop in this assignment, here are a few examples:
- HTTP web server
- A chat service, such as Google Hangouts or Slack
- Data delivery service, such as the GPS position data in the http://odss.mbari.org backend
Many successful businesses have been built by building rich applications on top of a TCP/IP service such as the one you will create in this assignment.

## Task
Your task is to write client code that satisfies the following requirements:

### Client code
There are two clients, X and Y (both essentially identical) that will communicate with a server. Clients X and Y will each open a TCP socket to your server and send a message to your server. The message contains the name of the client followed by your name (e.g., “Client X: Alice”, “Client Y: Bob”). 
Later when clients receive a message back from the server, they should print the message that they sent to the server, followed by the reply received from the server. The following figures explain the problem.

[Connection of clients to server](./imgs/figure1.png)

[Response of server to clients](./imgs/figure2.png)

The response message does not rely on the order of the connection establishment. If the connections are established in a different order the response will still be dependent only on the order of the messages:


[Reversed order of conect](./imgs/figure1.png)

### Server code
The server will accept connections from both clients and after it has received messages from both X and Y, the server will print their messages and then send an acknowledgment back to your clients. The acknowledgement from the server should contain the sequence in which the client messages were received (“X: Alice received before Y: Bob”, or “Y: Bob received before X: Alice”). After the server sends out this message it should output a message saying - “Sent acknowledgment to both X and Y”. Your server can then terminate. 
The server sits in an infinite loop listening for incoming TCP packets. When a packet comes, the server simply sends it back to the client. You can use the TCP server/client programs from the previous programming assignment as templates to start and then modify it to build your programming assignment.

### Expected output

Case 1: When you type a message from Client X first:


Case 2: When you type a message from Client Y first:


### Message Format
The messages in this assignment are formatted in a simple way. The client message must look like:
Client X: Alice
Client Y: Bob
The messages from server to client must look like (depending on the order of the received messages):
X: Alice received before Y: Bob
OR
Y: Bob received before X: Alice


## What to Hand in
1. You will hand in the complete client and server code. You only need one client program.
2. Minutes of the 3 meetings.
3. Make a pdf file with screenshots of server and client side output as shown in the expected output section. ***Please do not upload the screenshots as image files.***
  - Screenshots showing each client making a connection with the server separately (2 screenshots expected here).
  - Screenshots showing Client X  and Client Y (as established by the server) sending messages to the server separately in different order that is:
    - Client X sends a message to the server first then Client Y sends a message to the server. (2 screenshots expected here).
    - Client Y sends a message to the server first then Client X sends a message to the server. (2 screenshots expected here).

## Grading Criteria

### Client-specific requirements
- (5 points) You must use TCP sockets; you will need to establish a connection first, since it is a connection oriented protocol.
- (5 points) Clients must initiate the connection by sending their connection requests to the server one client at a time.

### Server-specific Requirements
- (5 points) The server must accept connections from both clients first BEFORE receiving the messages from either client.
- (5 points) Server establishes the first client that made a connection as Client X and the second one as client Y.
- (5 points) After establishing a connection with both Clients, Server sends a message to both clients stating that a connection has been established. The message from the server must indicate which client is X and which client is Y. (Message to clients must look like: “Client X connected” or “Client Y connected”.)
- (5 points) Server receives messages from both clients (in any order) and establishes which message it received first.
- (10 points) Server sends acknowledgements to both clients stating which message was received first. (Message to clients must look like: “Y: First_message received before X: Second_message” or “X: First_message received before Y: Second_message”.)
- (10 points) The response string from Server to Clients (“X: First_message received before Y: Second_message”, or “Y: First_message received before X: Second_message”) must be in the order the messages from Client X or Client Y are received at the server and NOT the order in which the clients X and Y connected to the server. 
  - ***Note: You will need multithreading and a way to share data between threads to achieve this.***
- (10 points) Your program should print out the messages received by the client and server at the receiving end.
- (10 points) Execute your programs on your mininet virtual machine. 
- (20 points) Explain why you need multithreading to solve this problem. Put this in a comment at the top of your server code.
- (10 points) Program must be well documented.
Teamwork grade: (50 points) Each team member will grade each other teammate out of 10 points during peer evaluation. I will average all team members’ grades and scale it to get your teamwork grade out of 50 points. Note that 30% of your grade will come from your teamwork and team member evaluations.

### Optional Extra-credit Exercises
The extra credit part of this assignment is mainly for fun​ and is Challenging. You can modify the above server-client to create a simple chat service. 
- (10 points) Clients X and Y can only chat through the server. For example, every message that client X sends to the server, the server relays to client Y and vice versa. 
- (5 points) When a client (say X) wants to exit the chat service it sends a “Bye” message. When a server sees a “Bye” message, it relays this message to Y and then terminates the connection to both clients. 
- (5 points) Each client (say X) should output the messages sent by it and those received from Y. As this is a chat service the number/content of messages exchanged is not fixed. So your clients should have the capability to accept inputs (which are the content of the messages) from the keyboard. 

### Example TCP Client-Server Code
The following code fully implements a capitalization server and client. You can use this as your starter code for this assignment.
Server Code

```
#TCPCapitalizationServer.py
from socket import *
serverPort = 12000

# Create a TCP socket
# Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET,SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while True:
     connectionSocket, addr = serverSocket.accept()  
     sentence = connectionSocket.recv(1024).decode()
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence.encode())
     connectionSocket.close()
```


Client Code
```
from socket import *
# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname
serverName = 'put your hostname here'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print ('From Server:', modifiedSentence.decode())
clientSocket.close()
```
