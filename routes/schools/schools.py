from flask_restful import Resource
from db import db

class Schools(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute("SELECT id, name from schools")
        schools = cursor.fetchall()
        return {"schools": schools}
