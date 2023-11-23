class Doctor:
    _c = None

    def __init__(self, db):
        self._c = db

    def getAll(self):
        res = self._c.execute("SELECT * FROM medecins WHERE deleted = 0")
        return res.fetchall()

    def find(self, id):
        res = self._c.execute("SELECT * FROM medecins WHERE ID = ?", (id,))
        return res.fetchone()

    def delete(self, id):
        self._c.execute("UPDATE medecins SET deleted = 1 WHERE ID = ?", (id,))
        self._c.commit()

    def add(self, prenom, nom):
        self._c.execute("INSERT INTO medecins (prenom, nom) VALUES (?, ?)", (prenom, nom))
        self._c.commit()