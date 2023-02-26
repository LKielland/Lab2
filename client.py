#Client side connects to the server and sends a message to everyone

import socket
import threading

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# write server ip and port, and connect
### write your code here ###
serverIP = input("Enter server IP: ")
clientPort = 12000
clientName = socket.gethostbyname(socket.gethostname())

addr = (serverIP, clientPort)
clientSocket.connect(addr)

username = input("Enter username: ")
clientSocket.send(username.encode())
### your code ends here ###

def receive_messages(clientSocket):
    while True:
        message = clientSocket.recv(1024).decode()
        if not message:
            break
        print(f"\r{' '*len(f'{username}: ')}\r{message}\n{username}: ", end="")
        
def send_messages(clientSocket):
    while True:
        message = input(f"{username}: ")
        clientSocket.send(message.encode())
        

# create two threads, one for receiving messages and one for sending messages
receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
send_thread = threading.Thread(target=send_messages, args=(clientSocket,))

# start the threads
receive_thread.start()
send_thread.start()

# wait for the threads to finish
receive_thread.join()
send_thread.join()

# close the client socket
clientSocket.close()