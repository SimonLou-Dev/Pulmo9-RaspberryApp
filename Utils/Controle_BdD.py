import sqlite3, datetime

class Controle_BdD:
    def __init__(self, nom_bdd):
        print("oui")
        self.__nom_bdd = nom_bdd
        self.__c = sqlite3.connect(self.__nom_bdd + '.db', check_same_thread=False)
        self.verifier_tables()

    def verifier_tables(self):
        self.__c.execute('''CREATE TABLE IF NOT EXISTS medecins (ID INTEGER PRIMARY KEY AUTOINCREMENT, nom text, prenom text, deleted INT DEFAULT 0)''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS patients (ID INTEGER PRIMARY KEY AUTOINCREMENT, nom text, prenom text, sexe text, date_naissance text, taille INT, poids INT)''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS mesures (ID INTEGER PRIMARY KEY AUTOINCREMENT, frequence INT, doctor_id INT, date_mesure DATETIME, patient_ID INT, REUSLT FLOAT NULLABLE DEFAULT NULL, running BOOLEAN DEFAULT 0)''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS mesures_details (ID INTEGER PRIMARY KEY AUTOINCREMENT, mesure_id INT, pression VARCHAR, debit VARCHAR)''')
        return True


    def connEstablished(self):
        return self.__c != None

    def getConnexion(self):
        return self.__c