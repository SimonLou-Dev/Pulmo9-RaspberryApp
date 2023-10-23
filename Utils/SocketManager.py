import eel
import json
import socket
import subprocess
import threading
import time

bl = False

try:
    import bluetooth
    bl = True
except:
    print("Bluetooth indispo")
    bl = False

class SocketManager:
    socketType = ""
    currentSocket = None
    connIsOk = False
    running = True
    __sendList = {}
    __seqNumber = 0
    __threads = []

    __pingLaunched = False
    __pingLaunchedTime = time.time()

    #Constructeur de la classe, BT par défaut pour une connexion bluetooth et local pour le dévellopement
    def __init__(self, _socketType = "bt"):
        if not bl and _socketType == "bt":
            raise Exception("Impossible d'établir une conenxtion avec le bluetooth")
        self.socketType = _socketType
        if _socketType == "bt":
            self.__btConnection()
        elif _socketType == "local":
            self.__DevConnection()
        self.currentSocket.settimeout(5)
        message = self.__CommandToSet("connection")
        self.__sendMessage(message)
        self.running = True
        self.__threads.append(threading.Thread(target=self.__listener))
        self.__threads.append(threading.Thread(target=self.__sendPing))
        for thread in self.__threads:
            thread.start()


    def stopBluetooth(self):
        self.running = False
        for thread in self.__threads:
            thread.join()
        print("Bluetooth stopped")
        self.currentSocket.close()


    # Convertit la command en un dictionnaire
    def __CommandToSet(self, command):
        x = {"command": command}
        return x

    #Methode privée pour la connexion bluetooth
    def __btConnection(self):
        print("TryBtConnexion")
        stdoutdata = subprocess.getoutput("hcitool con")
        if "00:18:E4:00:14:25" not in stdoutdata.split(): #Recherche de l'adresse MAC du serveur
            try:
                self.currentSocket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) #Création du socket
                self.currentSocket.connect(("00:18:E4:00:14:25", 1)) #Connexion au serveur
                print("Connexion établie")
            except Exception as erreur:
                print("Connexion échouée, restart and , send message to user")
                print(str(erreur))

    #Methode privée pour la connexion locale
    def __DevConnection(self):
        print("TryLocal")
        host = socket.gethostname() #Récupération de l'adresse IP du serveur
        port = 5000  # socket server port number
        self.currentSocket = socket.socket() #Création du socket
        self.currentSocket.connect((host, port)) #Connexion au serveur
        bufsize = self.currentSocket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        print ("Buffer size [Before]:%d" %bufsize)

    def __listener(self):
        print("[DEBUG] Démarage du thread d'écoutte")
        final = ""
        while self.running:
            data = self.currentSocket.recv(2048)
            recive =  data.decode()
            final += recive
            if(final.find("\r\n") != -1):
                print("income packet")
                incomeJson = json.loads(final)
                command = incomeJson["command"]
                if command == "connection:ACK":
                    self.connIsOk = True
                    print("Device connected")
                    eel.Auth_setBlConnected()
                elif command == "recive:ACK":
                    self.__markMessageAsRecived(incomeJson)
                    break
                elif command == "pong":
                    self.__markMessageAsRecived(incomeJson)
                    self.__pingLaunched = False
                    self.connIsOk = True
                    #Mettre à  jour l'interface en connecté
                else:
                    print("Unknown command")
                    break


    def __markMessageAsRecived(self, message):
        seq = message["seqNumber"]
        self.__sendList.pop(seq)

    def __sendMessage(self, message):
        message["seqNumber"] = self.__seqNumber
        self.__sendList[self.__seqNumber] = message
        self.__seqNumber += 1
        jsonStr = json.dumps(message)
        self.currentSocket.send(jsonStr.encode())


    #Fonction qui permet de vérifier létat de la connextion toutes les 120 secondes avec un timeout de 30Sec
    def __sendPing(self):

        while self.running:
            self.__pingLaunched = False #Ping en cours
            self.__pingLaunchedTime = time.time() #heure du démarage du dernier ping

            if time.time() - self.__pingLaunchedTime >= 120:
                command = self.__CommandToSet("ping")
                self.__sendMessage(command)
                self.__pingTimeStart = True
                self.__pingLaunchedTime = time.time()

            if self.__pingLaunched and time.time() - self.__pingLaunchedTime >= 30:
                self.connIsOk = False
                print("timeout")
                #Send une notif eel pour dire que la connexion est perdue



    #Methode pemettant de savoir si la connexion est établie
    def getConState(self):
        return self.connIsOk

    # Methode permettant d'envoyer les données de calibrage
    def configure(self, debit, pression):
        data = {"command": "calibrate", "debit": debit, "pression": pression}
        self.__sendMessage(data)

    # Methode permmettant de changer la fréquence de l'ampli
    def changeFrequency(self, freq):
        data = {"command": "changeFreq", "frequency": freq}
        self.__sendMessage(data)

    # Methode permettant de démarer une mesure
    def startMesure(self):
        data = self.__CommandToSet("startMesure")
        self.__sendMessage(data)

    def stopMesure(self):
        data = self.__CommandToSet("stopMesure")




