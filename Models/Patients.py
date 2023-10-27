from Models.Model import Model
import json

class Patients(Model):
    __c = None

    def __init__(self, db):
        self.__c = db

    def get_all_patients(self, page, search):
        pages = self.getNumberOfPages(search)

        if pages == 0:
            return {
                "patients": [],
                "pages": 0
            }

        res = self.__c.execute("SELECT * FROM patients WHERE nom LIKE '%" + search + "%' OR prenom LIKE '%" + search + "%' LIMIT 5 OFFSET " + str((int(page)-1) * 5))
        return {
            "patients": res.fetchall(),
            "pages": pages
        }

    def get_patient(self, id):
        res = self.__c.execute("SELECT * FROM patients WHERE id = ?", (id,))
        return res.fetchone()

    def add_patient(self, nom, prenom, date_naissance, poids, taille, sexe):
        self.__c.execute("INSERT INTO patients (nom, prenom, date_naissance, poids, taille, sexe) VALUES (?, ?, ?, ?, ?, ?)", (nom, prenom, date_naissance, poids, taille, sexe))
        self.__c.commit()

    def update_patient(self, id, nom, prenom, date_naissance, poids, taille, sexe):
        self.__c.execute("UPDATE patients SET nom = ?, prenom = ?, date_naissance = ?, poids = ?, taille = ?, sexe = ? WHERE id = ?", (nom, prenom, date_naissance, poids, taille, sexe, id))
        self.__c.commit()

    def getNumberOfPages(self, search):
        res = self.__c.execute("SELECT COUNT(*) FROM patients WHERE nom LIKE '%" + search + "%' OR prenom LIKE '%" + search + "%'")
        return int(res.fetchone()[0] / 5)
