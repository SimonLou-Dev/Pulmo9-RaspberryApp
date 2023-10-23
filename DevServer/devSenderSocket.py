import socket
       
host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number
currentSocket = socket.socket()
currentSocket.connect((host, port))

msg = input("ClientA: Entrez un message ou exit pour sortir:") 

while msg != 'exit':
    message = input("->")
    currentSocket.sendall(bytes(message + "\n\r\n", 'UTF-8'))
    if message == "exit":
        break;

currentSocket.close()