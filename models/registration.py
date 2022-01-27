from db import getConnection

class RegistrationModel:
    def __init__(self, config):
        self.contestantId = config['contestantId']
        self.teamId = config['teamId']
        self.game = config['game']
        self.nickname = config['nickname']
        if 'role' in config:
            self.role = config['role']
        else:
            self.role = None
        if 'externist' in config:
            self.externist = config['externist']
        else:
            self.externist = False

    @classmethod
    def exists(cls, contestant_id, game):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        query = "SELECT id FROM registrations WHERE contestantId = %(contestant_id)s AND game= %(game)s"
        values = (contestant_id, game)
        cursor.execute(query, {'game': game, 'contestant_id': contestant_id})
        row = cursor.fetchone()
        cursor.close()
        db.close()
        if row: 
            return True
        else:
            return False

    def insert(self):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        query = "INSERT INTO registrations (contestantId, nickname, teamId, game, externist, role) VALUES(%s, %s, %s, %s, %s, %s)"
        values = (self.contestantId, self.nickname, self.teamId, self.game, self.externist, self.role)
        cursor.execute(query, values)
        cursor.close()
        db.close()

        