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

    def ajouter_patient(self, patient):
        recherche = self.__c.execute("SELECT count(*) FROM patients WHERE nom = ? AND prenom = ? AND date_naissance = ?", (patient[0], patient[1], patient[3]))
        if recherche.fetchone()[0] <= 0:
            self.__c.execute("INSERT INTO patients(nom,prenom,sexe,date_naissance, taille, poids) VALUES ('" + patient[0] + "','" + patient[1] +"','" + patient[2] +"','" + patient[3] + "','" + patient[4] + "','" + patient[5] + "')")
            self.__c.commit()
        else:
            return "Erreur, le patient existe déjà."

    def modifier_patient(self, patient):
        return

    def supprimer_patient(self, patient):
        self.__c.execute("DELETE FROM patients WHERE nom = ? AND prenom = ? AND date_naissance = ?", (patient[0], patient[1], patient[2]))
        return

    def liste_patients(self):
        recherche = self.__c.execute("SELECT nom, prenom, sexe, date_naissance FROM patients")
        resultats = recherche.fetchall()
        return resultats
        
    def ajouter_mesure(self, mesure, patient):
        type_de_mesure = mesure[0][0]
        praticien_ID = mesure[0][1]
        date_mesure = str(datetime.datetime.now())
        patient_ID = str(patient["ID"])
        tableau_pression = ','.join([str(press_float) for press_float in mesure[1]])
        tableau_debit = ','.join([str(deb_float) for deb_float in mesure[2]])
        self.__c.execute("INSERT INTO mesures(type_de_mesure, praticien_ID, date_mesure, patient_ID, tableau_pression, tableau_debit) VALUES '" + type_de_mesure + "','" + praticien_ID + "','" + date_mesure + "','" + patient_ID + "','" + tableau_pression + "','" + tableau_debit + "')")
        self.__c.commit()
        print(mesure, patient)
        return

    def supprimer_mesure(self, mesure):
        return

    def ajouter_medecin(self, medecin):
        recherche = self.__c.execute("SELECT count(*) FROM medecins WHERE nom = ? AND prenom = ?", (medecin[0], medecin[1]))
        if recherche.fetchone()[0] > 0:
            return "Erreur, le médecin existe déjà."
        else:
            self.__c.execute("INSERT INTO medecins(nom, prenom) VALUES ('" + medecin[0] + "','" + medecin[1] + "')")
            self.__c.commit()

    def modifier_medecin(self, medecin):
        return

    def supprimer_medecin(self, medecin):
        self.__c.execute("DELETE FROM medecins WHERE nom = ? AND prenom = ?", (medecin[0], medecin[1]))
        self.__c.commit()
        return

    def liste_medecins(self):
        recherche = self.__c.execute("SELECT * FROM medecins")
        table_medecin_mesure = []
        for medecin in recherche.fetchall():
            table_medecin_mesure.append(medecin[1] + " " + medecin[2])
        return table_medecin_mesure

    def lecture_constantes(self):
        frequence_bdd = self.__c.execute("SELECT frequence_haut_parleur FROM parametres")
        try:
            frequence = frequence_bdd.fetchall()[0][0]
        except:
            print("Erreur lors de la lecture de la fréquence en BDD, initialisation à 4Hz")
            frequence = 4
        duree_mesure_bdd = self.__c.execute("SELECT duree_mesure FROM parametres")
        try:
            duree_mesure = duree_mesure_bdd.fetchall()[0][0]
        except:
            print("Erreur lors de la lecture de la duree de mesure en BDD, initialisation à 30s")
            duree_mesure = 30
        self.modifier_constantes([frequence, duree_mesure])
        return [frequence, duree_mesure]

    def modifier_constantes(self, constantes):
        frequence = constantes[0]
        duree_mesure = constantes[1]
        try:
            self.__c.execute("INSERT INTO parametres(ID, frequence_haut_parleur, duree_mesure) VALUES (?, ?, ?)", (1, frequence, duree_mesure))
            self.__c.commit()
        except Exception as e:
            self.__c.execute("UPDATE parametres SET frequence_haut_parleur = ?, duree_mesure = ? WHERE ID = 1", (frequence, duree_mesure))
            self.__c.commit()

    def lecture_calibrage(self):
        dernier_calibrage_bdd = self.__c.execute("SELECT * FROM calibrage")
        dernier_calibrage = dernier_calibrage_bdd.fetchall()[0]
        print(dernier_calibrage)
        return dernier_calibrage

    def modifier_calibrage(self, calibrage):
        pression = calibrage[0]
        debit = calibrage[1]
        try:
            self.__c.execute("INSERT INTO calibrage(ID, date_dernier_calibrage, gain_debit, gain_pression) VALUES (?, ?, ?, ?)", (1, datetime.date.today(), pression, debit))
            self.__c.commit()
        except Exception as e:
            self.__c.execute("UPDATE calibrage SET date_dernier_calibrage = ?, gain_debit = ?, gain_pression = ? WHERE ID = 1", (datetime.date.today(), pression, debit))
            self.__c.commit()
            
    def liste_mesures(self, nom, prenom, sexe, date_naissance):
        recherche = self.__c.execute("SELECT ID FROM patients WHERE nom = ? AND prenom = ? AND sexe = ? AND date_naissance = ?", (nom, prenom, sexe, date_naissance))
        patient_id = recherche.fetchone()
        if patient_id is not None:
            recherche = self.__c.execute("SELECT * FROM mesures WHERE patient_id = ?", (patient_id[0],))
            liste_mesures_bdd = []
            for mesures_patient in recherche.fetchall():
                recherche_medecin = self.__c.execute("SELECT * FROM medecins WHERE ID = ?", (mesures_patient[3],))
                medecin_id = recherche_medecin.fetchone()
                if medecin_id is not None:
                    medecin_mesure = medecin_id[1] + ' ' + medecin_id[2]
                else:
                    medecin_mesure = "Médecin inconnu"
                liste_mesures_bdd.append([mesures_patient[1], mesures_patient[2], medecin_mesure, mesures_patient[4], "Volume moyen", "Débit moyen"])
            return liste_mesures_bdd
        else:
            return None
        
