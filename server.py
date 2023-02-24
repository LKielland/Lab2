"""
Server side: it simultaneously handle multiple clients
and broadcast when a new client joins or a client
sends a message.
"""
import socket
import _thread as thread
import time
import sys
#this is too keep all the newly joined connections! 
all_client_connections = []
def now():
    """
    returns the time of day
    """
    return time.ctime(time.time())

def handleClient(connection: socket.socket, addr):
    """
    a client handler function 
    """
    
    username = connection.recv(2048).decode()
    sender = connection.getpeername()

    #this is where we broadcast everyone that a new client has joined
    ### Write your code here ###
    # append this to the list for broadcast
    all_client_connections.append(connection)

    # create a message to inform all other clients
    joinMessage = "just joined the chat"
    
    # that a new client has just joined.
    broadcast(joinMessage, sender, username)
    ### Your code ends here ###
    
    while True:
        message = connection.recv(2048).decode()
        print (now() + " " +  str(addr) + "#  ", message)
        if (message == "exit" or not message):
            ### Write your code here ###
            quitMessage = "just left the chat"
            #broadcast this message to the others
            broadcast(quitMessage, sender, username)
            ### Your code ends here ###
            break
        else:
            broadcast(message, sender, username)
            
    connection.close()
    all_client_connections.remove(connection)

def broadcast(message, sender, username):
    print ("Broadcasting")
    ### Write your code here ###
    for connection in all_client_connections:
        if connection.getpeername() != sender:
            connection.sendall(f"[{username}]: {message}".encode())
    ### Your code ends here ###

def main():
    """
    creates a server socket, listens for new connections,
    and spawns a new thread whenever a new connection join
    """
    serverPort = 12000
    serverName = socket.gethostbyname(socket.gethostname())
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (serverName, serverPort)
    
    try:
        # Use the bind function wisely!
        serverSocket.bind(addr)
    except socket.error as e: 
        print("Bind failed. Error : Guru Meditation #%s" % e)
        sys.exit()
    serverSocket.listen(10)
    print ('The server is ready to receive')
    while True:
        ### Write your code here ###
        connectionSocket, addr =   serverSocket.accept() # accept a connection

        print(f"[ACTIVE CONNECTIONS] {thread._count() + 1}")
        ### You code ends here ###
 
        print('Server connected by ', addr) 
        print('at ', now())
        thread.start_new_thread(handleClient, (connectionSocket,addr)) 
    serverSocket.close()
    

if __name__ == '__main__':
    main()