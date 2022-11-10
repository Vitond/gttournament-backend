from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from models.contestant import ContestantModel
from models.registration import RegistrationModel
from constants import GAMES

from routes.registration.validation import AloneRegistrationValidation

from utils.are_regs_closed import are_regs_closed

class AloneRegistration(Resource):
    def post(self):
        if are_regs_closed():
            return "Registrace je již uzavřena", 400

        data = request.get_json()
        schema = AloneRegistrationValidation()
        try:
            schema.load(data)
        except ValidationError as err:
            return {"messages": err.messages}, 400

        contestant_data = data['contestant']

        if not 'schoolId' in data:
            return "Chybí id školy", 400

        print('sutu')
        if data['game'] == 'COUNTER_STRIKE':
            if not 'csRank' in contestant_data:
                return "Chybí pole csrank", 400
            if not 'maxCsRank' in contestant_data:
                return "Chybí pole maxCsRank", 400
            if not 'faceitLevel' in contestant_data:
                return "Chybí pole faceitLevel", 400
            if not 'maxFaceitLevel' in contestant_data:
                return "Chybí pole maxFaceitLevel"
       
        if data['game'] == 'ROCKET_LEAGUE':
            if not 'epicId' in contestant_data:
                return "Chybí pole epicId, 400"
                
        existing_contestant_id = ContestantModel.find_id_by_email(contestant_data['email'])
        if existing_contestant_id:
            contestant_id = existing_contestant_id
            contestant = ContestantModel.find_by_id(existing_contestant_id)
        else:
            new_contestant = ContestantModel(contestant_data)
            new_contestant.insert()
            contestant = new_contestant
            contestant_id = ContestantModel.find_id_by_email(contestant_data['email'])
        if (RegistrationModel.exists(contestant_id, data['game'])):
            return "Registration already exists", 400
        else:
            registration = RegistrationModel({
                'nickname': contestant_data['nickname'],
                'teamId': None,
                'game': data['game'],
                'contestantId': contestant_id
            })
            registration.insert()
        if existing_contestant_id:

            if data['game'] == 'ROCKET_LEAGUE':
                contestant.update({'epicId': contestant_data['epicId']})

            if data['game'] == 'COUNTER_STRIKE':
                contestant.update({
                    'csRank': contestant_data['csRank'],
                    'maxCsRank': contestant_data['maxCsRank'],
                    'faceitLevel': contestant_data['faceitLevel'],
                    'maxFaceitLevel': contestant_data['maxFaceitLevel']
                })
        
       