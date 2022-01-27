from flask_restful import Resource
from db import getConnection

class Contestants(Resource):
    def get(self):
        db = getConnection()
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * from teams")
        teams = cursor.fetchall()
        returnedTeams = []
        for team in teams:
            teamId = team[0]
            query = "SELECT nickname, role FROM registrations WHERE teamId = %s"
            values = (teamId, )
            cursor.execute(query, values)
            members = cursor.fetchall()
            returnedTeams.append({"team": team, "members": members})
        cursor.close()
        db.close()
        return {"teams": returnedTeams}
