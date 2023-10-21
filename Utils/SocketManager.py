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
    __sendList = {}
    __seqNumber = 0

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

        print("Waiting for ConnCallBack")
        self.__WaitForConn() #Attente de la réponse du serveur

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

    
    # Methode privée pour attendre la réponse du serveur
    def __WaitForConn(self):
        callBackConn = threading.Thread(target = self.__listenCallBack)
        callBackConn.start()
        
    #Methode privée pour écouter la réponse du serveur utilsée en thread
    def __listenCallBack(self):
        recived = False
        time_start = time.time()
    
        while not recived:
            recive = None
            try:
                data = self.currentSocket.recv(2048)
                recive =  data.decode()

            except:
                recive = ""

            if len(recive) == 0:
                continue

            decodeMessage = self.__decodeMessage(recive)

            if decodeMessage == "":
                continue

            if decodeMessage["command"] == "connection:ACK":
                recived = True
                self.connIsOk = True
                print("Device connected")
                eel.Auth_setBlConnected()
                return True

            if time.time() - time_start > 20: #Si le temps d'attente est dépassé, la connexion est échouée
                print("Connexion échouée")
                recived = True
                break

    def __sendMessage(self, message):
        message["seqNumber"] = self.__seqNumber
        self.__sendList[self.__seqNumber] = message
        self.__seqNumber += 1
        jsonStr = json.dumps(message)
        self.currentSocket.send(jsonStr.encode())

    def __decodeMessage(self, recivedMessage):
        try:
            recivedMessage = json.loads(recivedMessage)
        except Exception as e:
            print(e)

        if("seqNumber" in  self.__sendList):
            self.__sendList.pop(recivedMessage["seqNumber"])
            return recivedMessage

        return ""


    #Fonction qui permet de vérifier létat de la connextion toutes les 120 secondes avec un timeout de 30Sec
    def __startPingPong(self):
        time_start = time.time()
        launched = False
        launchedTime = time.time()
        if time.time() - time_start >= 120:  # Si le temps d'attente est dépassé, la connexion est échouée
            command = self.__CommandToSet("ping")
            self.__sendMessage(command)
            launched = True
            launchedTime = time.time()

        if launched and time.time() - launchedTime >= 30:
            print("timeout")
            self.connIsOk = False

        try:
            data = self.currentSocket.recv(2048)
            recive = data.decode()

        except:
            recive = ""

        try:
            recive = json.loads(recive)
        except Exception as e:
            print(e)

        if recive["command"] == "pong":  # Si la réponse est positive, la connexion est
            seq = recive["seqNumber"]
            self.__sendList.pop(seq)
            launched = False
            self.connIsOk = True

    #Methode pemettant de savoir si la connexion est établie
    def getConState(self):
        return self.connIsOk

    # Methode permettant d'envoyer les données de calibrage
    def configure(self, debit, pression):
        data = {"command": "calibrate", "debit": debit, "pression": pression}
        self.__sendMessage(data)
        self.__waitACK()

    # Methode permmettant de changer la fréquence de l'ampli
    def changeFrequency(self, freq):
        data = {"command": "changeFreq", "frequency": freq, "seqNumber": self.__seqNumber}
        self.__sendMessage(data)
        self.__waitACK()

    # Methode permettant de démarer une mesure
    def startMesure(self):
        data = self.__CommandToSet("startMesure")
        self.__sendMessage(data)
        self.__waitACK()
        self.__readMesureData()

    def stopMesure(self):
        data = self.__CommandToSet("stopMesure")
        self.__sendMessage(data)
        self.__waitACK()

    # Methode permettant de lire les données de mesures et de les envoyer à son Model, (renvoi un ACK)
    def __readMesureData(self):
        stopped = False
        time_start = time.time()
        while not stopped:
            recive = None
            try:
                data = self.currentSocket.recv(2048)
                recive = data.decode()
            except:
                recive = ""

            if len(recive) == 0:
                continue

            try:
                recive = json.loads(recive)
            except Exception as e:
                print(e)

            if recive["command"] == "sendData":  # Si la commande est send  data je lis sinon tant pis
                if recive["ended"] == True: stopped = True  # Si c'est la dernière mesure qui est envoyé

                print(recive["data"])
                # Données dans recive["data"]

    # Methode permettant d'attendre la confirmation de lecture
    def __waitACK(self):
        ackRecive = False

        while not ackRecive:
            recive = None
            try:
                data = self.currentSocket.recv(2048)
                recive = data.decode()
            except:
                recive = ""

            if len(recive) == 0:
                continue

            try:
                recive = json.loads(recive)
            except Exception as e:
                print(e)

            if recive["command"] == "recive:ACK":  # Si la commande est l'acknoledgement je ferme la boucle et je quitte
                seq = recive["seqNumber"]
                self.__sendList.pop(seq)
                ackRecive = True
                return
