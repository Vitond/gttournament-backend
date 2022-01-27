from db import getConnection

class TeamModel:
    def __init__(self, name, game, schoolId):
        self.name = name
        self.game = game
        self.schoolId = schoolId

    def json(self):
        return {'name': self.name, 'game': self.game}

    def insert(self):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        query = "INSERT INTO teams (name, game, schoolId) VALUES (%s, %s, %s)"
        values = (self.name, self.game, self.schoolId)
        cursor.execute(query, values)
        cursor.close()
        db.close()

    @classmethod
    def find_id_by_name(cls, name):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        query = "SELECT id from teams WHERE name=%s"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        cursor.close()
        db.close()
        if row:
            return row[0]
        else:
            return None
            

