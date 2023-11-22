import eel, threading, time, sys

from Utils.Logger import Logger
from Utils.SocketManager import SocketManager
from Utils.Controle_BdD import Controle_BdD
from Models.Doctor import Doctor
from Models.Patients import Patients
from Models.Mesures import Mesures



running = True;
eel_thread = None
logger = Logger()
current_logged = None

database = Controle_BdD("database").getConnexion()

try:


    if len(sys.argv) > 1 and sys.argv[1] == "--dev":
        bl_conn = SocketManager(eel, database, "local")
    else:
        bl_conn = SocketManager(eel, database)

except Exception as e:
    print(e)
    running = False
    sys.exit()

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
    doctor = Doctor(database).find(id)
    if doctor != None:
        current_logged = id
        return {"logged": True, "doctor": doctor}
    else:
        return {"logged": False, "doctor": doctor}

# logout(callback)

#  get_patients(string search = "", int page = 0)
@eel.expose
def get_patients(search = "", page = 0):
    return Patients(database).get_all_patients(page, search)


# get_patient(int id)
@eel.expose
def get_patient(id):
    return Patients(database).get_patient(id)


# create_patient(string nom, string prenom, date DDN, float taille, float poid, int sexe = 0, int id = 0)
@eel.expose
def create_patient(nom, prenom, DDN, taille, poid, sexe = 0, id = 0):
    if id == 0 or id == "0":
        return Patients(database).add_patient(nom, prenom, DDN, taille, poid, sexe)
    else:
        Patients(database).update_patient(id, nom, prenom, DDN, taille, poid, sexe)
        return True

@eel.expose
def calibrate_pression(pression):
    #TODO: Faire la calibration
    return True

@eel.expose
def calibrate_pression_atm():
    #TODO: Faire la calibration
    return True


# list_mesure(int patient_id)
@eel.expose
def list_mesure(patient_id, page):
    return Mesures(database).get_patient_mesures(patient_id, page)

# create_mesure(int patient_id, int  frequency)
@eel.expose
def create_mesure(patient_id, frequency):
    return Mesures(database).create_mesure(frequency, current_logged, time.time(), patient_id)

# start_mesure(int mesure_id)

# init_mesure(int mesure_id)

# stop_mesure(int mesure_id)

# update_current_mesure(int mesure_id)
@eel.expose
def update_current_mesure(mesure_id):
    return Mesures(database).get_mesure_points(mesure_id)


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










