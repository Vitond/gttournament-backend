from db import getConnection

class ContestantModel:
    @classmethod
    def find_by_id(cls, id):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        query = "SELECT id, name, surname, email, discord, schoolId, adult, epicId, csRank, maxCsRank, faceitLevel, maxFaceitLevel FROM contestants WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        row = cursor.fetchone()
        cursor.close()
        db.close()
        if row:
            return cls({
                'name': row[1],
                'surname': row[2],
                'email': row[3],
                'discord': row[4],
                'schoolId': row[5],
                'adult': row[6],
                'epicId': row[7],
                'csRank': row[8],
                'maxCsRank': row[9],
                'faceitLevel': row[10],
                'maxFaceitLevel': row[11]
            })
        else:
            return None
    @classmethod
    def find_id_by_email(cls, email):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        query = "SELECT id FROM contestants WHERE email = %s"
        values = (email,)
        cursor.execute(query, values)
        row = cursor.fetchone()
        cursor.close()
        db.close()
        if row:
            return row[0]
        else:
            return None
            
    def insert(self):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        query = "INSERT INTO contestants (name, surname, adult, email, discord, csRank, maxCsRank, faceitLevel, maxFaceitLevel, epicId, schoolId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.name, self.surname, self.adult, self.email, self.discord, self.csRank, self.maxCsRank, self.faceitLevel, self.maxFaceitLevel, self.epicId, self.schoolId)
        cursor.execute(query, values)
        cursor.close()
        db.close()

    def update(self, config):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        if 'epicId' in config:
            query = "UPDATE contestants SET epicId = %s WHERE email = %s"
            values = (config['epicId'], self.email)
            cursor.execute(query, values)
        if 'csRank' in config:
            query = "UPDATE contestants SET csRank = %s WHERE email = %s"
            values = (config['csRank'], self.email)
            cursor.execute(query, values)
        if 'maxCsRank' in config:
            query = "UPDATE contestants SET maxCsRank = %s WHERE email = %s"
            values = (config['maxCsRank'], self.email)
            cursor.execute(query, values)
        if 'faceitLevel' in config:
            query = "UPDATE contestants SET faceitLevel = %s WHERE email = %s"
            values = (config['faceitLevel'], self.email)
            cursor.execute(query, values)
        if 'maxFaceitLevel' in config:
            query = "UPDATE contestants SET maxFaceitLevel = %s WHERE email = %s"
            values = (config['maxFaceitLevel'], self.email)
            cursor.execute(query, values)
        cursor.close()
        db.close()

    def __init__(self, config):
        self.name = config['name']
        self.surname = config['surname']
        self.schoolId = config['schoolId']
        self.discord = config['discord']
        self.email = config['email']
        self.csRank = ''
        self.maxCsRank = ''
        self.epicId = ''
        self.faceitLevel = None
        self.maxFaceitLevel = None

        if 'csRank' in config:
            self.csRank = config['csRank']
        if 'epicId' in config:
            self.epicId = config['epicId']
        if 'maxCsRank' in config:
            self.maxCsRank = config['maxCsRank']
        if 'faceitLevel' in config:
            self.faceitLevel = config['faceitLevel']
        if 'maxFaceitLevel' in config:
            self.maxFaceitLevel = config['maxFaceitLevel']
        self.adult = config['adult']
