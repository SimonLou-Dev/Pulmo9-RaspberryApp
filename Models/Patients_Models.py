from Models.Model import Model
import json

class Patients_Models(Model):
    nom = None
    prenom = None
    sexe = None
    date_naissance = None
    taille = None
    poids = None

    def __init__(self, db):
        super().__init__(db)
        self.__bdd = db.getConnexion()

    def paginate_mesure(self, page):
        res = self.__bdd.execute("SELECT * FROM mesures LIMIT 15 OFFSET " + str(page * 15))
        res.fecthall()

        return json.loads(res)

    def paginate_patient(self, search, page):
        res = self.__bdd.execute("SELECT * FROM patients WHERE nom LIKE '%" + search + "%' OR prenom LIKE '%" + search + "%' LIMIT 15 OFFSET " + str(page * 15))
        res.fecthall()
        return json.loads(res)
