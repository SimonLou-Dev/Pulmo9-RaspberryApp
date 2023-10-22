import json, socket, subprocess

buffer = ''

stdoutdata = subprocess.getoutput("hcitool con")
if "00:18:E4:00:14:25" not in stdoutdata.split(): #Recherche de l'adresse MAC du serveur
    try:
        socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) #Création du socket
        socket.connect(("00:18:E4:00:14:25", 1)) #Connexion au serveur
        print("Connexion établie")
    except Exception as erreur:
        print("Connexion échouée, restart and , send message to user")
        print(str(erreur))
        socket = None

while True and socket != None:
    data = socket.recv(1024)
    if not data:
        break

        # add the current data read by the socket to a temporary buffer
    buffer += data

    # search complete messages
    messages = buffer.split('\r\r')

    # we need at least 2 messages to continue
    if len(messages) == 1:
        continue

    # seperator found, iterate across complete messages
    for message in messages [:-1]:
        # handle here the message
        print message

    # set the buffer with the last cutted message
    buffer = messages [-1]