# Localhost Multi-Client Chat Application Using TCP Sockets in Python



A Python chatroom application that can connect multiple clients to a localhost central server over TCP, allowing users to send and receive messages in real time.



## Description



This program is a multi-client chat application using TCP sockets in Python. The system consists of a centralized server and multiple clients communicating through the client-server model. Each client connects directly to the server, sending chat messages to the server, and the server then forwards (broadcasts) those messages to all other connected clients. Clients will chose a unique username to identify them upon connection. Clients do not communicate with each other directly; all message traffic flows through the server. The server supports multiple simultaneous client connections and handle message delivery in real time. A client can join or leave the chat without affecting the remaining clients' communication.



## Design Overview



I started designing the program with just creating the server sockets and client sockets in their respective server.py and client.py files. My program code creates sockets with localhost as the host as the messaging system only works between terminals on the same pc. I chose 9999 as the arbitrary port number, since some smaller port numbers are reserved for other uses. In client.py, I created two functions and threads, the first function is for awaiting user input to send messages and the second is waiting for incoming messages from the server. For server.py, there are 3 functions, one for sending messages to all connected clients, the second for awaiting any incoming messages (a separate thread is created for each connected client as any client can send a message to the server), and the third for accepting any clients who want to connect. My server.py has a dictionary that keeps track of connected clients using the clientsocket as dictionary key and username as value, which I would then use to check for existing and deny repeated usernames. The client dictionary is also used when a message is submitted by a client, the server loops through it and sends the message to all connected clients. I put a loop that ran forever inside all the functions and would call break when I needed to disconnect them. That way, the code allows for any amount of clients to connect, any amount of messages to be sent and received at any time. To handle disconnections, I had to put all the code logic inside try and except blocks as during the disconnect process, error messages would pop up due to the forever looping thread functions. So using the try except blocks cleanly handled those situations and I was able to disconnect the client and servers properly by removing the client from the client dictionary in the server.py as well as sending disconnect messages.



## Getting Started



### Dependencies



\* Python



### Installing



\* Download client.py and server.py, ensure they are in the same folder.



### Executing program



\* Open terminal and run "python server.py" to start the server.

\* On another terminal window, run "python client.py" to create a client and it will automatically try to connect to the server.

\* If the client connects to the server successfully, it will then prompt the client for a unique username. If the username is not in use, the client will successfully connect.

\* You can connect as many clients as you want.

\* To send messages, simply type it in the terminal and press Enter, and it will be sent to the server and show up on all clients.

