from Models.Model import Model
import json, math

class Mesures(Model):
    _c = None
    _table = "mesures"

    def __init__(self, db):
        self._c = db


    def get_patient_mesures(self, patient_id, page = 0):
        MaxPages = self.__get_mesures_pages(patient_id)
        if MaxPages == 0:
            return {
                "mesures": [],
                "pages": 0
            }

        res = self._c.execute("SELECT * FROM mesures WHERE patient_ID =" + patient_id +" ORDER BY date_mesure DESC LIMIT 5 OFFSET " + str((int(page)-1) * 5))
        return {
            "mesures": res.fetchall(),
            "pages": MaxPages
        }
        #TODO : Eloquant pour récuprérer le DR

    def __get_mesures_pages(self, patient_id):
        res = self._c.execute("SELECT COUNT(*) FROM mesures WHERE patient_ID = " + patient_id)
        return math.ceil(res.fetchone()[0] / 5)

    def get_mesure(self, mesure_id):
        res = self._c.execute("SELECT * FROM mesures WHERE ID = ?", (mesure_id,))
        return res.fetchone()

    def create_mesure(self, frequence, doctor_id, date_mesure, patient_ID):
        self._c.execute("INSERT INTO mesures (frequence, doctor_id, date_mesure, patient_ID) VALUES (?, ?, ?, ?)", (frequence, doctor_id, date_mesure, patient_ID))
        self._c.commit()
        return self.get_mesure(self.getLastInsertId())


    def start_save_mesure(self, mesure_id):
        self._c.execute("INSERT INTO mesures_details (mesure_id, pression, debit) VALUES (?, '[]', '[]')", (mesure_id, 0, 0))
        self._c.commit()

    def save_mesure_points(self, mesure_id, debit, pression):
        self._c.execute("UPDATE mesures_details SET pression = ?, debit = ? WHERE mesure_id = ?", (pression, debit, mesure_id))
        self._c.commit()

    def get_mesure_points(self, mesure_id):
        res = self._c.execute("SELECT debit, pression FROM mesures_details WHERE mesure_id = ?", (mesure_id,))
        return res.fetchone()
