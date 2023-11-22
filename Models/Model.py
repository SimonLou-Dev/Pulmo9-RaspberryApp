import json
class Model:
    id = None
    __db = None

    def __init__(self, db):
        self.__db = db

    def save(self):
        #parse les attibutes
        self.__bdd.execute()

    def delete(self):
        if self.id != None:
            self.__bdd.execute("DELETE FROM " + self.__table + " WHERE id = " + str(self.id))

    def getLastInsertId(self):
        res = self.__bdd.execute("SELECT MAX(id) FROM " + self.__table)
        return res.fetchone()[0]

    def find_id(self, id):
        res = self.__bdd.execute("SELECT * FROM " + self.__table + " WHERE id = " + str(id))
        res.fecthall()
        #Vérifier le contenue de la variable et mettre l'ID dans les attibuts
        return json.loads(res)