from Models.Model import Model
import json

class Patients(Model):
    __c = None

    def __init__(self, db):
        self.__c = db

    def get_all_patients(self, page, search):
        res = self.__c.execute("SELECT * FROM patients WHERE nom LIKE '%" + search + "%' OR prenom LIKE '%" + search + "%' LIMIT 15 OFFSET " + str(page * 15))
        return res.fecthall()

    def get_patient(self, id):
        res = self.__c.execute("SELECT * FROM patients WHERE id = ?", (id,))
        return res.fetchone()

    def add_patient(self, nom, prenom, date_naissance, poids, taille, sexe):
        self.__c.execute("INSERT INTO patients (nom, prenom, date_naissance, poids, taille, sexe) VALUES (?, ?, ?, ?, ?, ?)", (nom, prenom, date_naissance, poids, taille, sexe))
        self.__c.commit()

    def update_patient(self, id, nom, prenom, date_naissance, poids, taille, sexe):
        self.__c.execute("UPDATE patients SET nom = ?, prenom = ?, date_naissance = ?, poids = ?, taille = ?, sexe = ? WHERE id = ?", (nom, prenom, date_naissance, poids, taille, sexe, id))
        self.__c.commit()
