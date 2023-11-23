import json
class Model:
    _c = None
    _table = None

    def __init__(self, db):
        self._c = db

    def delete(self, id):
        if self.id != None:
            self._c.execute("DELETE FROM " + self._table + " WHERE id = " + str(self.id))

    def getLastInsertId(self):
        res = self._c.execute("SELECT MAX(id) FROM " + self._table)
        return res.fetchone()[0]

    def find_id(self, id):
        res = self._c.execute("SELECT * FROM " + self._table + " WHERE id = " + str(id))
        res.fecthall()
        #Vérifier le contenue de la variable et mettre l'ID dans les attibuts
        return json.loads(res)