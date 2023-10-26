class Doctor:
    __c = None

    def __init__(self, db):
        self.__c = db

    def getAll(self):
        res = self.__c.execute("SELECT * FROM medecins WHERE deleted = 0")
        return res.fetchall()

    def find(self, id):
        res = self.__c.execute("SELECT * FROM medecins WHERE ID = ?", (id,))
        return res.fetchone()

    def delete(self, id):
        self.__c.execute("UPDATE medecins SET deleted = 1 WHERE ID = ?", (id,))
        self.__c.commit()

    def add(self, prenom, nom):
        self.__c.execute("INSERT INTO medecins (prenom, nom) VALUES (?, ?)", (prenom, nom))
        self.__c.commit()