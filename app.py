from flask import Flask, jsonify, request, abort

from flask_restful import Resource, Api
from utils.register_routes import register_routes

# ROUTES
from routes.schools import schoolsRoutes
from routes.registration import registrationRoutes

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    register_routes(api, schoolsRoutes, '/schools')
    register_routes(api, registrationRoutes, '/registration')
    app.run(port=5000)


    






