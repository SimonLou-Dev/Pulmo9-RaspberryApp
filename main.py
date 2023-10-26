import eel, threading, time, sys

from Utils.Logger import Logger
from Utils.SocketManager import SocketManager
from Utils.Controle_BdD import Controle_BdD
from Models.Doctor import Doctor


running = True;
eel_thread = None
logger = Logger()
current_logged = None





try:
    bl_conn = SocketManager(eel,"local")
except Exception as e:
    print(e)
    running = False
    sys.exit()

database = Controle_BdD("database").getConnexion()

#Creation de l'objet eel en mode wb et en authorisant les extensions .js et .html


##Initialiser la connexion BL
#Rajouter un callBack qui permet de mettre à jour dans eel


## Démarage de l'app


##Start la connexion à la BDD


#Fonctions qui permettent à l'eel de communiquer

@eel.expose
def sendClose():
    logger.print("Main", 1, "Demande de fermeture de l'application")
    running = False
    bl_conn.stopBluetooth()
    #Close la connexion à la BDD
    logger.print("Main", 1, "Processus backend terminé")


# get_doctors(void)
@eel.expose
def get_doctors():
    return Doctor(database).getAll()

# remove_doctor(int id)
@eel.expose
def remove_doctor(id):
    Doctor(database).delete(id)
    return True

# add_doctor(string prenom, string nom)
@eel.expose
def add_doctor(prenom, nom):
    Doctor(database).add(prenom, nom)
    return True

# login(id)
@eel.expose
def login(id):
    if Doctor(database).find(id) != None:
        current_logged = id
        return True
    else:
        return False

# logout(callback)

#  get_patients(string search = "", int page = 0)

# get_patient(int id)

# create_patient(string nom, string prenom, date DDN, float taille, float poid, int sexe = 0, int id = 0)

# list_mesure(int patient_id)

# start_mesure(int patient_id, int  frequency)

# stop_mesure(int mesure_id)

# update_current_mesure(int mesure_id)

# calibrate(int pression, int debit)

# set_freq(int frequency);

#Fin des fonction eel exportés

#Début des call vers le JS

@eel.expose
def get_socket_status():
    return bl_conn.getConState()





#Fonction qui permet de lancer le serveur en arrière plan Après l'éxecution de tout ce qu'il y a avant;
# /!\ Attention : C'est  bloquant
if len(sys.argv) > 1 and sys.argv[1] == "--dev":
    eel.init("client")
    eel.start({"port": 5173, "host":"127.0.0.1"}, host="127.0.0.1", port=8888) #, cmdline_args=['--kiosk']
else:
    eel.init("web")
    eel.start('./', port=8888, mode="chrome")










