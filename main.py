import eel, threading, time, sys
from Utils.SocketManager import SocketManager

running = True;

#Creation de l'objet eel en mode wb et en authorisant les extensions .js et .html
eel.init('web', allowed_extensions=['.js', '.html'])

##Initialiser la connexion BL
#Rajouter un callBack qui permet de mettre à jour dans eel
try:
    bl_conn = SocketManager("local")
except Exception as e:
    print(e)
    running = False
    sys.exit()

## Démarage de l'app
eel.start('templates/index.html',jinja_templates="templates", block=False) #, cmdline_args=['--kiosk']

##Start la connexion à la BDD


#Fonctions qui permettent à l'eel de communiquer

# get_doctors(void)

# remove_doctor(int id)

# add_doctor(string prenom, string nom)

# login(callBack)

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

#Fin des fonction eel


#Fonction qui permet de lancer le serveur en arrière plan Après l'éxecution de tout ce qu'il y a avant;
# /!\ Attention : C'est  bloquant
while running:
    eel.sleep(1);






