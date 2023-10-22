import json, socket, subprocess



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


final = ""
while True and socket != None:

    message = socket.recv(16384)
    message = message.decode()
    final += message

    if(final.find("\r\n") != -1):
        print(final)
        print(json.loads(final))
        final = ""