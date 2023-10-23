
import json
import socket
import subprocess
import threading
import time
from Utils.Logger import Logger


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

    __eel= None

    __logger = Logger()

    __pingLaunched = False
    __pingLaunchedTime = time.time()

    #Constructeur de la classe, BT par défaut pour une connexion bluetooth et local pour le dévellopement
    def __init__(self, eel, _socketType = "bt"):
        self.__eel = eel
        if not bl and _socketType == "bt":
            raise Exception("Impossible d'établir une conenxtion avec le bluetooth")
        self.socketType = _socketType
        if _socketType == "bt":
            self.__btConnection()
        elif _socketType == "local":
            self.__DevConnection()
        self.currentSocket.settimeout(600)
        message = self.__CommandToSet("connection")
        self.__sendMessage(message)
        self.running = True
        self.__threads.append(threading.Thread(target=self.__listener))
        self.__threads.append(threading.Thread(target=self.__sendPing))
        for thread in self.__threads:
            thread.start()


    def stopBluetooth(self):
        self.running = False
        self.__logger.print("SocketManager", 1, "Attente de la fermeture de la connexion bluetooth")
        for thread in self.__threads:
            thread.join(1)
        self.__logger.print("SocketManager", 1, "Fermeture de la connexion bluetooth")
        self.currentSocket.close()


    # Convertit la command en un dictionnaire
    def __CommandToSet(self, command):
        x = {"command": command}
        return x

    #Methode privée pour la connexion bluetooth
    def __btConnection(self):
        self.__logger.print("SocketManager", 1, "Tentative de connexion bluetooth")
        stdoutdata = subprocess.getoutput("hcitool con")
        if "00:18:E4:00:14:25" not in stdoutdata.split(): #Recherche de l'adresse MAC du serveur
            try:
                self.currentSocket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) #Création du socket
                self.currentSocket.connect(("00:18:E4:00:14:25", 1)) #Connexion au serveur
                self.__logger.print("SocketManager", 1, "Connecté à l'appareil bluetooth")
            except Exception as erreur:
                self.__logger.print("SocketManager", 3, "Impossible d'ouvrir la connexion bluetooth")
                print(str(erreur))

    #Methode privée pour la connexion locale
    def __DevConnection(self):
        self.__logger.print("SocketManager", 1, "Connexion au socket AF INET")
        host = socket.gethostname() #Récupération de l'adresse IP du serveur
        port = 5000  # socket server port number
        self.currentSocket = socket.socket() #Création du socket
        self.currentSocket.connect((host, port)) #Connexion au serveur


    def __listener(self):
        self.__logger.print("SocketManager", 1, "Ecoute des messages arrivants")
        final = ""
        while self.running:
            print("Current status "  + self.running.__str__())
            try:
                data = self.currentSocket.recv(2048)
            except Exception as e:
                print(e)
                continue
            if not data:
                continue
            recive =  data.decode()
            final += recive
            print("C'est un bon ? " + final.find("\r\n").__str__())
            if(final.find("\r\n") != -1):
                print("Je suis dans le message")
                incomeJson = json.loads(final)
                command = incomeJson["command"]
                if command == "connection:ACK":
                    self.connIsOk = True
                    self.__logger.print("SocketManager", 1, "Connexion confirmée")
                    self.__eel.bl_is_connected()
                elif command == "recive:ACK":
                    self.__markMessageAsRecived(incomeJson)
                    break
                elif command == "pong":
                    self.__logger.print("SocketManager", 1, "Appreil toujours connecté")
                    self.__markMessageAsRecived(incomeJson)
                    self.__pingLaunched = False
                    self.connIsOk = True
                    #Mettre à  jour l'interface en connecté
                else:
                    self.__logger.print("SocketManager", 2, "Commande inconnue")
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




