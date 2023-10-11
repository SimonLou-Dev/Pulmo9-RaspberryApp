import socket, subprocess, time, threading, json, eel

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
        message = self.__CommandToJSON("connection")
        self.currentSocket.send(message.encode()) #Envoi de la confirmation de connexion
        print("Waiting for ConnCallBack")
        self.__WaitForConn() #Attente de la réponse du serveur

    def __CommandToJSON(self, command):
        x = {"command": command}
        return json.dumps(x)

    #Methode privée pour la connexion bluetooth
    def __btConnection(self):
        print("TryBtConnexion")
        stdoutdata = subprocess.getoutput("hcitool con")
        if "98:D3:11:FC:84:44" not in stdoutdata.split(): #Recherche de l'adresse MAC du serveur
            try:
                self.currentSocket = bluetooth.BluetoothSocket( bluetooth.RFCOMM ) #Création du socket bluetooth
                self.currentSocket.connect(("98:D3:11:FC:84:44", 1)) #Connexion au serveur

            except Exception as erreur:
                print("Connexion échouée, nouvel essai")
                print(str(erreur))

    #Methode privée pour la connexion locale
    def __DevConnection(self):
        print("TryLocal")
        host = socket.gethostname() #Récupération de l'adresse IP du serveur
        port = 5000  # socket server port number
        self.currentSocket = socket.socket() #Création du socket
        self.currentSocket.connect((host, port)) #Connexion au serveur
        
    
    #Methode privée pour attendre la réponse du serveur
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

            try:
                recive = json.loads(recive)
            except Exception as e:
                print(e)

            if recive["command"] == "connection:ACK": #Si la réponse est positive, la connexion est établie
                recived = True
                self.connIsOk = True
                print("Device connected")
                eel.Auth_setBlConnected()
                return True

            if time.time() - time_start > 20: #Si le temps d'attente est dépassé, la connexion est échouée
                print("Connexion échouée")
                recived = True
                break

    #Mettre dans une boucle
    def __startPingPong(self):
        time_start = time.time()
        launched = False
        launchedTime = time.time()
        if time.time() - time_start >= 120:  # Si le temps d'attente est dépassé, la connexion est échouée
            self.__CommandToJSON("ping")
            launched = True
            launchedTime = time.time()

        if launched and time.time() - launchedTime >= 30:
            print("timeout")

        try:
            data = self.currentSocket.recv(2048)
            recive = data.decode()

        except:
            recive = ""

        try:
            recive = json.loads(recive)
        except Exception as e:
            print(e)

        if recive["command"] == "pong":  # Si la réponse est positive, la connexion est établie
            launched = False


    #Methode pemettant de savoir si la connexion est établie
    def getConState(self):
        return self.connIsOk
        

