from Models.Model import Model
import json

class Mesures(Model):
    __c = None

    def __init__(self, db):
        self.__c = db


    def get_patient_mesures(self, patient_id):
        res = self.__c.execute("SELECT * FROM mesures WHERE patient_ID = ?", (patient_id,))
        return res.fetchall()

    def get_mesure(self, mesure_id):
        res = self.__c.execute("SELECT * FROM mesures WHERE ID = ?", (mesure_id,))
        return res.fetchone()

    def create_mesure(self, frequence, doctor_id, date_mesure, patient_ID):
        self.__c.execute("INSERT INTO mesures (frequence, doctor_id, date_mesure, patient_ID, pression_atm, running) VALUES (?, ?, ?, ?, ?, true)", (frequence, doctor_id, date_mesure, patient_ID))
        self.__c.commit()

        #TODO return id


    def start_save_mesure(self, mesure_id):
        self.__c.execute("INSERT INTO mesures_details (mesure_id, pression, debit) VALUES (?, '[]', '[]')", (mesure_id, 0, 0))
        self.__c.commit()

    def save_mesure_points(self, mesure_id, debit, pression):
        self.__c.execute("UPDATE mesures_details SET pression = ?, debit = ? WHERE mesure_id = ?", (pression, debit, mesure_id))
        self.__c.commit()

    def get_mesure_points(self, mesure_id):
        res = self.__c.execute("SELECT * FROM mesures_details WHERE mesure_id = ?", (mesure_id,))
        return res.fetchone()
