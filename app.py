from flask import Flask, jsonify, request, abort

from flask_restful import Resource, Api
from utils.register_routes import register_routes

# ROUTES
from routes.schools import schoolsRoutes
from routes.registration import registrationRoutes
from routes.contestants import contestantsRoutes
app = Flask(__name__)

if __name__ == "__main__":
    
    api = Api(app)

    register_routes(api, schoolsRoutes, '/schools')
    register_routes(api, registrationRoutes, '/registration')
    register_routes(api, contestantsRoutes, '/contestants')
    app.run(port=5000)


    






