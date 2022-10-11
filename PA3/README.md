# Programming Assignment 3
## CST 311, Introduction to Computer Networks

READ INSTRUCTIONS CAREFULLY BEFORE YOU START THE ASSIGNMENT.

Assignment must be submitted electronically to [Canvas](https://csumb.instructure.com/) by 11:59 p.m. on the due date.  Late assignments will not be accepted. 
Use the Teams on the Programming Assignment Teams document (also on Canvas under General Information -> Team Information)
Select your Team leader and divide up work per the Programming Process instructions (also on Canvas under General Information > Team Information.)

The assignment requires you to submit both client and server programs. The naming convention of the file should be `PA3_Server_Team<your team #>.py` and `PA3_Client_Team<your team #>.py`.
Additionally, put your names in the program header, where indicated in the `__credits__` variable.
Your client and server programs must meet the requirements below. Your program must have sufficient comments to clearly explain how your code works. Your code must compile to get partial credit.

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
Your task is to write client and server code that satisfies the following requirements:

### Client code
There are two identical clients that will both communicate with the server.
Each will open a TCP socket to the server and will send a message to it based on user input.
When they send their message they should print the text of the message being sent to the server.
Later when the clients receive a message back from the server they should print the response from the server.

### Server code

The server will accept connections from both clients and wait for messages from each.
The first client to establish a connection to the server will be referred to as "X" and the second client to connect to the server will be referred to as "Y".
When the server has received messages from both the clients[^1] it will respond to both clients with a message consistent of the messages received from both clients in the order that they were received in.

For example, if client X sends message "Hello!" and then client Y sends the message "Howdy!" then the client response is "X: 'Hello!', Y: 'Howdy!".
See [example images](#example-images) for details

### Example Images

The first example shows the client on the left establishing a connection and sending a message, `Hello!` before the client on the right connects and sends its message `Howdy!`.
Therefore, the message from the server to both clients reads `X: 'Hello!', Y:'Howdy'`. 

<img src="imgs/comm_example_1.png" height="400" alt="Connection of clients to server (example 1)">

---

The second example shows the client on the left establishing a connection first but waits to send its message of `Hello!` until after the client on the right establishes a connection and sends its message of `Howdy!`.
Therefore, the message from the server to both clients reads `Y: 'Howdy!', X: 'Hello!'`.
Note that the order of the messages recieved has changed.


<img src="./imgs/comm_example_2.png" height="400" alt="Connection of clients to server (example 2)">

---

In this final example, the right-hand client establishes a connection before the left-hand client, and also sends a message before it.
We now see the message from the server to both client reads `X: 'Howdy!', Y: 'Hello!'`.
Note that the client identifiers has changed.

<img src="./imgs/comm_example_3.png" height="400" alt="Connection of clients to server (example 3)">

### Message Format
The messages in this assignment are formatted in a simple way. The client message must consist of a simple text message (e.g. `Hello!` or `Howdy!` or some other string read in from the user).
The messages from the server to the client must look like (depending on the order of connection establishment and received messages -- see [Example Images](example-images) for details): `X: 'Hello!', Y:'Howdy'`


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
The extra credit part of this assignment is mainly for fun and is challenging.
You can modify the above server-client to create a simple chat service. 
- (10 points) Clients X and Y can only chat through the server. For example, every message that client X sends to the server, the server relays to client Y and vice versa. 
- (5 points) When a client (say X) wants to exit the chat service it sends a “Bye” message. When a server sees a “Bye” message, it relays this message to Y and then terminates the connection to both clients. 
- (5 points) Each client (say X) should output the messages sent by it and those received from Y. As this is a chat service the number/content of messages exchanged is not fixed. So your clients should have the capability to accept inputs (which are the content of the messages) from the keyboard. 

### Starter code

Starter code can be found in the [src](src) directory.

[^1]: Only the first message from each client is required to be stored but if you want to capture more it can be a fun challenge!
