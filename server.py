#imports for us to be able to use threading and sockets
import socket
import threading

#userClients will be a dictionary that i will use to map client sockets to usernames
userClients = {}

def sendMessage(message):
    #this function will send messages to all the clients

    #loops thru all the currently connected clients and sends the message to all of em
    for clientsocket, clientname in userClients.items():
        #print(clientsocket) 
        #print(clientname)
        clientsocket.send(message.encode("utf-8"))

def awaitMessage(username, clientsocket):
    #this function will wait for a client to send a message
    while(1):
        try:
            message = clientsocket.recv(1024).decode("utf-8")

            #if the message was a quit message, we remove the client from our userclient dictionary and close client socket
            #otherwise, we take the message and send it to all connected clients
            if(message == "QUIT"):
                sendMessage(username + " has left the server.")
                print(username + " has left the server.")
                userClients.pop(clientsocket)
                clientsocket.shutdown(socket.SHUT_WR)
                clientsocket.close()
                break
            else:
                sendMessage(username + ": " + message)
        
        #if there was an exception with recieving a message, we just disconnect the client
        except Exception:
            sendMessage(username + " has left the server.")
            print(username + " has left the server.")
            #check if clientsocket still exists in the userClient dictionary and remove it if so
            if(clientsocket in userClients):
                userClients.pop(clientsocket)
                clientsocket.shutdown(socket.SHUT_WR)
                clientsocket.close()
            break

def acceptClients():
    #this functions will run forever allowing clients to join
    while(1):
        try:
            #accept any clients connecting
            (clientsocket, address) = serversocket.accept()

            #the first message recieved from a connected client will be it's username, but we will need to check if the username is already in use
            #we loop until we get a unique username, inform the client its valid or not, and then add to the userClient dictionary with the client socket
            validName = False
            username = ""
            while(validName != True):
                validName = True
                username = clientsocket.recv(1024).decode("utf-8")

                #loops thru all the currently connected clients and checks for matches
                for checkingSocket, checkingname in userClients.items():
                    if(username == checkingname):
                        validName = False
                        clientsocket.send("Not valid".encode("utf-8"))
            
            clientsocket.send("Valid".encode("utf-8"))
            userClients[clientsocket] = username

            print(username + " has connected.")
            sendMessage(username + " has connected.")

            #i create a thread that will handle clients sending messages
            acceptClientThread = threading.Thread(target=awaitMessage, args=(username, clientsocket, ))
            acceptClientThread.start()
        
        #handle exceptions such as if the server is closed
        except Exception:
            break

# create an INET, STREAMing socket, which is tcp because sock stream is TCP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# bind the socket to local host (your local pc) and a well-known port
serversocket.bind(('localhost', 9999))
# become a server socket
serversocket.listen(5)

#i create a thread that will handle clients joining
acceptClientThread = threading.Thread(target=acceptClients)
acceptClientThread.start()

while(1):
    if(input("You are the server admin. Type input \"QUIT\" to close the server.\n") == "QUIT"):
        #after the server gets an input, it will send a message to all clients and then close the server
        sendMessage("The server has been terminated so all connections will be closed.")
        print("Server is now closed.")

        # closes all the client sockets
        for clientsocket, username in userClients.items():
            clientsocket.shutdown(socket.SHUT_RDWR)
            clientsocket.close()
        userClients.clear() 

        serversocket.close()
        break