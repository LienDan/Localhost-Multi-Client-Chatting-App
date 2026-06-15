#imports for us to be able to use threading and sockets
import socket
import threading

def awaitMessage(clientsocket):
    #this function will handle the server sending messages back to the client
    while(1):
        try:
            response = clientsocket.recv(1024).decode("utf-8")
            if not response:
                print("You have disconnected from the server.")
                break
            print(response)

        except Exception:
            print("You have disconnected from the server.")
            break

def sendMessage(clientsocket):
    #this function will handle taking client inputs and sending it to the server, as well as handling QUIT
    while(1):
        message = input("")
        try:
            clientsocket.send(message.encode("utf-8"))
            if(message == "QUIT"):
                clientsocket.shutdown(socket.SHUT_RDWR) # shutsdown the socket so no more read or writes
                clientsocket.close()
                break
        
        except Exception:
            print("You have disconnected from the server.")
            break


# create an INET, STREAMing socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#trys to connect to the server and if it doesn't work, it'll print an error and quit
try:
    # now connect to local host pc on port 9999 (arbitrary number)
    clientsocket.connect(("localhost", 9999))
except ConnectionRefusedError:
    print("Connection failed: make sure the server is running before running the client.")
    raise SystemExit

#asks user for username but loops until username is valid
validUsername = False
username = ""
while(validUsername != True):
    username = input("Enter your username: ")
    # Send username
    clientsocket.send(username.encode("utf-8"))

    #will get response from server saying if username is valid or not
    response = clientsocket.recv(1024).decode("utf-8")

    if(response == "Valid"):
        validUsername = True
    if(response == "Not valid"):
        print("Username is in use. Please select another username.")

print("You have connected to the server as " + username + ". Type QUIT to quit the program.")

#i create a thread that will handle clients joining
awaitThread = threading.Thread(target=awaitMessage, args=(clientsocket, ))
awaitThread.start()

#i create a thread that will handle typing and sending messages
sendMessageThread = threading.Thread(target=sendMessage, args=(clientsocket, ))
sendMessageThread.start()

