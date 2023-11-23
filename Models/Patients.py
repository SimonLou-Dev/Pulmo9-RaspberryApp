from Models.Model import Model
import json, math

class Patients(Model):
    _c = None
    _table = "patients"

    def __init__(self, db):
        self._c = db



    def get_all_patients(self, page, search):
        pages = self.getNumberOfPages(search)

        if pages == 0:
            return {
                "patients": [],
                "pages": 0
            }

        res = self._c.execute("SELECT id, prenom, nom, date_naissance, sexe FROM patients WHERE nom LIKE '%" + search + "%' OR prenom LIKE '%" + search + "%' OR date_naissance LIKE '%" + search + "%'  LIMIT 5 OFFSET " + str((int(page)-1) * 5))
        return {
            "patients": res.fetchall(),
            "pages": pages
        }

    def get_patient(self, id):
        res = self._c.execute("SELECT * FROM patients WHERE id = ?", (id,))
        return res.fetchone()

    def add_patient(self, nom, prenom, date_naissance, poids, taille, sexe):
        self._c.execute("INSERT INTO patients (nom, prenom, date_naissance, poids, taille, sexe) VALUES (?, ?, ?, ?, ?, ?)", (nom, prenom, date_naissance, poids, taille, sexe))
        self._c.commit()
        return self.get_patient(self.getLastInsertId())


    def update_patient(self, id, nom, prenom, date_naissance, poids, taille, sexe):
        self._c.execute("UPDATE patients SET nom = ?, prenom = ?, date_naissance = ?, poids = ?, taille = ?, sexe = ? WHERE id = ?", (nom, prenom, date_naissance, poids, taille, sexe, id))
        self._c.commit()
        return self.get_patient(id)

    def getNumberOfPages(self, search):
        res = self._c.execute("SELECT COUNT(*) FROM patients WHERE nom LIKE '%" + search + "%' OR prenom LIKE '%" + search + "%' OR date_naissance LIKE '%" + search + "%'")
        return math.ceil(res.fetchone()[0] / 5)
