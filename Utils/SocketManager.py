import socket, subprocess, time, threading

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
        message = "Conn:OK"
        self.currentSocket.send(message.encode()) #Envoi de la confirmation de connexion
        print("Waiting for ConnCallBack")
        self.__WaitForConn() #Attente de la réponse du serveur

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
                recive = data.decode()
            except:
                recive = recive
                
 
            if recive == "ConnCallBack:ok": #Si la réponse est positive, la connexion est établie
                recived = True
                self.connIsOk = True
                print("Device connected")
                return True
            if time.time() - time_start > 20: #Si le temps d'attente est dépassé, la connexion est échouée
                print("Connexion échouée")
                recived = True
                break
    
    #Methode pemettant de savoir si la connexion est établie
    def getConState(self):
        return self.connIsOk
        

