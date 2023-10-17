import sqlite3, datetime

class Controle_BdD:
    def __init__(self, nom_bdd):
        print("oui")
        self.__nom_bdd = nom_bdd
        self.__c = sqlite3.connect(self.__nom_bdd + '.db')

    def verifier_tables(self):
        self.__c.execute('''CREATE TABLE IF NOT EXISTS medecins (ID INTEGER PRIMARY KEY AUTOINCREMENT, nom text, prenom text, identifiant text, password text)''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS patients (ID INTEGER PRIMARY KEY AUTOINCREMENT, nom text, prenom text, sexe text, date_naissance text, taille INT, poids INT)''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS parametres (ID INTEGER PRIMARY KEY AUTOINCREMENT, frequence_haut_parleur INT, duree_mesure INT)''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS calibrage (ID INTEGER PRIMARY KEY AUTOINCREMENT, date_dernier_calibrage text, gain_debit INT, gain_pression INT)''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS mesures (ID INTEGER PRIMARY KEY AUTOINCREMENT, type_de_mesure text, praticien_ID INT, date_mesure text, patient_ID INT, tableau_debit text, tableau_debit text)''')
        return True


    def connEstablished(self):
        return self.__c != None

    def getConnexion(self):
        return self.__c